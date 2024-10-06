import argparse
import json
import logging
import pickle
import re
from pathlib import Path
from typing import Any

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

# List of special variables
SPECIAL_VARS = [
    "PNR",
    "SENR",
    "CPR",
    "CVR",
    "PNR12",
    "AEGTE_ID",
    "E_FAELLE_ID",
    "FAR_ID",
    "MOR_ID",
    "FAMILIE_ID",
    "ARBGNR",
    "ARBNR",
    "RECNUM",
    "PK_MFR",
    "FK_MFR",
    "YDERNR",
    "CPR_BARN",
    "CPR_FADER",
    "CPR_MODER",
]

# Fixed output directory
OUTPUT_DIRECTORY = Path("/path/to/your/fixed/output/directory")


def read_file(file_path: Path) -> pl.DataFrame:
    try:
        if file_path.suffix.lower() == ".parquet":
            return pl.read_parquet(file_path, memory_map=True)
        elif file_path.suffix.lower() == ".csv":
            # Read a small sample to determine encoding
            with open(file_path, "rb") as f:
                sample = f.read(1024)  # Read first 1024 bytes

            encodings = ["utf-8", "iso-8859-1", "windows-1252"]
            for encoding in encodings:
                try:
                    sample.decode(encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                encoding = "utf8-lossy"  # Default to lossy UTF-8 if no encoding works

            return pl.read_csv(
                file_path,
                encoding=encoding,
                null_values=["", "NULL", "null", "NA", "na", "NaN", "nan"],
                ignore_errors=False,
                low_memory=False,
                sample_size=10000,  # Increase sample size for better type inference
                infer_schema=False,  # Force all columns as strings
            )
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
    except Exception as e:
        logger.exception(f"Error reading file {file_path}: {e!s}")
        return pl.DataFrame()


def process_file(file_path: Path) -> dict[str, Any]:
    try:
        df = read_file(file_path)
        file_stem = file_path.stem

        # Updated regex to handle both "priv_sksube2012" and "ras2000" patterns
        match = re.match(r"([a-zA-Z_]+)(\d+)", file_stem)

        if match:
            register_name = (
                match.group(1).lower().rstrip("_")
            )  # Remove trailing underscore if present
            year = match.group(2)
            output_filename = f"{year}.parquet"
        else:
            register_name = file_stem.lower()
            year = ""
            output_filename = f"{register_name}.parquet"  # Use the full filename if no year is present

        output_path = OUTPUT_DIRECTORY / "registers" / register_name / output_filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if output_path.exists():
            existing_df = pl.read_parquet(output_path)
            if df.equals(existing_df):
                logger.info(
                    f"Skipping {file_path.name}: Output file already exists and content is identical"
                )
                return {}

        # Write directly to the output path
        df.write_parquet(output_path)

        # Verify the written data
        read_back_df = pl.read_parquet(output_path)
        if not df.equals(read_back_df):
            raise ValueError(
                "Verification failed: written data does not match original data"
            )

        logger.info(f"Processed {file_path.name} -> {output_path}")

        return {
            register_name: {
                year or register_name: {
                    "file_name": file_path.name,
                    "num_rows": len(df),
                    "num_columns": len(df.columns),
                    "column_names": df.columns,
                }
            }
        }

    except Exception as e:
        logger.exception(f"Error processing file {file_path}: {e!s}")
        return {}


def process_registers(
    input_directory: Path, progress: Progress, task: TaskID
) -> dict[str, Any]:
    results: dict[str, dict[str, Any]] = {}
    files = list(input_directory.rglob("*.parquet")) + list(
        input_directory.rglob("*.csv")
    )

    progress_file = OUTPUT_DIRECTORY / "progress.pkl"
    if progress_file.exists():
        with open(progress_file, "rb") as f:
            processed_files = pickle.load(f)
    else:
        processed_files = set()

    total_files = len(files)
    progress.update(task, total=total_files)

    for file_path in files:
        file_result = process_file(file_path)

        if file_result:  # If processing was successful
            for register, data in file_result.items():
                if register not in results:
                    results[register] = {}
                results[register].update(data)
            processed_files.add(str(file_path))
        else:
            logger.warning(
                f"Failed to process {file_path}. Will retry in the next run."
            )

        with open(progress_file, "wb") as f:
            pickle.dump(processed_files, f)

        progress.update(task, advance=1)

    return results


def save_summary(summary: dict[str, Any], output_file: Path) -> None:
    try:
        with open(output_file, "w") as f:
            json.dump(summary, f, indent=2)
        logger.info(f"Summary saved to {output_file}")
    except Exception as e:
        logger.exception(f"Error saving summary to {output_file}: {e!s}")


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
    parser.add_argument(
        "--summary_file",
        type=str,
        default="register_summary.json",
        help="Path to the summary file",
    )
    args = parser.parse_args()

    input_directory = Path(args.input_directory)
    summary_file = Path(args.summary_file)

    try:
        with Progress() as progress:
            task = progress.add_task("[green]Processing registers...", total=None)
            summary = process_registers(input_directory, progress, task)

        save_summary(summary, summary_file)

        print_summary_table(summary)

        logger.info("[bold green]Processing complete!")
        logger.info(f"[bold blue]Total registers processed: {len(summary)}")
        logger.info(f"[bold blue]Summary saved to: {summary_file}")
        logger.info(f"[bold blue]Parquet files saved to: {OUTPUT_DIRECTORY}/registers")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e!s}")


if __name__ == "__main__":
    main()
