import argparse
import json
import logging
import re
from pathlib import Path
from typing import Any

import chardet
import polars as pl
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, TaskID
from rich.table import Table

# Set up rich console
console = Console()

# Set up logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "profile_data.log"

# Create a logger
logger = logging.getLogger("profile_data")
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = RichHandler(console=console, rich_tracebacks=True)
file_handler = logging.FileHandler(log_file, encoding="utf-8")

# Create formatters and add it to handlers
console_format = logging.Formatter("%(message)s")
file_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Fixed output directory
OUTPUT_DIRECTORY = Path("/path/to/your/fixed/output/directory")


def detect_encoding(file_path: Path) -> str:
    # Read up to 1MB of the file
    with open(file_path, "rb") as file:
        raw_data = file.read(1000000)

    # Try chardet first
    result = chardet.detect(raw_data)
    if result["encoding"] is not None and result["confidence"] > 0.7:
        return result["encoding"]

    # If chardet fails or has low confidence, try common encodings
    common_encodings = ["utf-8", "iso-8859-1", "windows-1252", "ascii"]
    for encoding in common_encodings:
        try:
            raw_data.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            continue

    # If all else fails, default to UTF-8
    logger.warning(
        f"Could not confidently detect encoding for {file_path}. Defaulting to UTF-8."
    )
    return "utf-8"


def read_file(file_path: Path) -> pl.DataFrame:
    try:
        if file_path.suffix.lower() == ".parquet":
            return pl.read_parquet(file_path)
        elif file_path.suffix.lower() == ".csv":
            encoding = detect_encoding(file_path)
            return pl.read_csv(
                file_path,
                encoding=encoding,
                null_values=["", "NULL", "null", "NA", "na", "NaN", "nan"],
                ignore_errors=False,
                low_memory=False,
                sample_size=10000,
                infer_schema=False,
            )
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
    except Exception as e:
        logger.exception(f"Error reading file {file_path}: {e!s}")
        return pl.DataFrame()


def process_file(file_path: Path, summary: dict[str, Any]) -> None:
    try:
        df = read_file(file_path)
        file_stem = file_path.stem

        # Updated regex to handle both "priv_sksube2012" and "ras2000" patterns
        match = re.match(r"([a-zA-Z_]+)(\d+)", file_stem)

        if match:
            register_name = match.group(1).lower().rstrip("_")
            year = match.group(2)
            output_filename = f"{year}.parquet"
        else:
            register_name = file_stem.lower()
            year = ""
            output_filename = f"{register_name}.parquet"

        output_path = OUTPUT_DIRECTORY / "registers" / register_name / output_filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Check if the existing Parquet file is empty or failed
        if (
            output_path.exists() and output_path.stat().st_size <= 1_048_576
        ):  # 1 MB threshold
            logger.warning(f"Deleting empty or failed Parquet file: {output_path}")
            output_path.unlink()

        # Write directly to the output path
        df.write_parquet(output_path)

        # Verify the written data
        read_back_df = pl.read_parquet(output_path)
        if not df.equals(read_back_df):
            raise ValueError(
                "Verification failed: written data does not match original data"
            )

        logger.info(f"Processed {file_path.name} -> {output_path}")

        # Update summary
        if register_name not in summary:
            summary[register_name] = {}
        summary[register_name][year or register_name] = {
            "file_name": file_path.name,
            "num_rows": len(df),
            "num_columns": len(df.columns),
            "column_names": df.columns,
        }

        # Save summary after each file is processed
        save_summary(summary, Path("register_summary.json"))

    except Exception as e:
        logger.exception(f"Error processing file {file_path}: {e!s}")


def process_registers(
    input_directory: Path, progress: Progress, task: TaskID
) -> dict[str, Any]:
    summary: dict[str, dict[str, Any]] = {}
    files = list(input_directory.rglob("*.parquet")) + list(
        input_directory.rglob("*.csv")
    )

    total_files = len(files)
    progress.update(task, total=total_files)

    for file_path in files:
        process_file(file_path, summary)
        progress.update(task, advance=1)

    return summary


def save_summary(summary: dict[str, Any], output_file: Path) -> None:
    with output_file.open("w") as f:
        json.dump(summary, f, indent=2)
    logger.info(f"Summary updated in {output_file}")


def print_summary_table(summary: dict[str, Any]) -> None:
    table = Table(title="Processing Summary")
    table.add_column("Register", style="cyan")
    table.add_column("Year", style="magenta")
    table.add_column("File Name", style="green")
    table.add_column("Rows", justify="right", style="yellow")
    table.add_column("Columns", justify="right", style="yellow")

    for register, years in summary.items():
        for year, data in years.items():
            table.add_row(
                register,
                year,
                data["file_name"],
                str(data["num_rows"]),
                str(data["num_columns"]),
            )

    console.print(table)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert CSV/Parquet files to Parquet and generate summary."
    )
    parser.add_argument("input_directory", type=str, help="Path to the input directory")
    args = parser.parse_args()

    input_directory = Path(args.input_directory)

    try:
        with Progress() as progress:
            task = progress.add_task("[green]Processing registers...", total=None)
            summary = process_registers(input_directory, progress, task)

        print_summary_table(summary)

        logger.info("[bold green]Processing complete!")
        logger.info(f"[bold blue]Total registers processed: {len(summary)}")
        logger.info("[bold blue]Summary saved to: register_summary.json")
        logger.info(f"[bold blue]Parquet files saved to: {OUTPUT_DIRECTORY}/registers")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e!s}")


if __name__ == "__main__":
    main()
