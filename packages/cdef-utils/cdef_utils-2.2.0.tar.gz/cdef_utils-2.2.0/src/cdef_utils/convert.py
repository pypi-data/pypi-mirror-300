import argparse
import logging
import multiprocessing
import re
from pathlib import Path
from typing import Any

import polars as pl
import pyarrow.parquet as pq
import ujson
from charset_normalizer import from_bytes
from rich.console import Console
from rich.live import Live
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text

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

# Precompile regex pattern
FILE_PATTERN = re.compile(r"([a-zA-Z_]+)(\d+)")


def detect_encoding_incrementally(file_path: Path) -> str:
    with open(file_path, "rb") as file:
        result = from_bytes(file.read()).best()

    if result is None:
        return "utf-8"

    return result.encoding


def read_file(file_path: Path) -> pl.DataFrame:
    try:
        if file_path.suffix.lower() == ".parquet":
            return pl.read_parquet(file_path)
        elif file_path.suffix.lower() == ".csv":
            encoding = detect_encoding_incrementally(file_path)
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


def write_parquet_fast(df: pl.DataFrame, path: Path) -> None:
    arrow_table = df.to_arrow()
    pq.write_table(arrow_table, path)


def process_file(
    file_path: Path, summary: dict[str, Any]
) -> tuple[str, str, dict[str, Any]] | None:
    try:
        file_stem = file_path.stem

        match = FILE_PATTERN.match(file_stem)

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

        if output_path.exists():
            if output_path.stat().st_size <= 1_048_576:  # 1 MB threshold
                logger.warning(
                    f"Deleting small Parquet file for reprocessing: {output_path}"
                )
                output_path.unlink()
            else:
                logger.info(f"Skipping already processed file: {file_path}")
                df = pl.read_parquet(output_path)
                return (
                    register_name,
                    year,
                    {
                        "file_name": file_path.name,
                        "num_rows": len(df),
                        "num_columns": len(df.columns),
                        "column_names": df.columns,
                    },
                )

        df = read_file(file_path)

        write_parquet_fast(df, output_path)

        read_back_df = pl.read_parquet(output_path)
        if not df.equals(read_back_df):
            raise ValueError(
                "Verification failed: written data does not match original data"
            )

        logger.info(f"Processed {file_path.name} -> {output_path}")

        return (
            register_name,
            year,
            {
                "file_name": file_path.name,
                "num_rows": len(df),
                "num_columns": len(df.columns),
                "column_names": df.columns,
            },
        )

    except Exception as e:
        logger.exception(f"Error processing file {file_path}: {e!s}")
        return None


def process_files_parallel(
    files: list[Path], summary: dict[str, Any], num_processes: int | None = None
) -> None:
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(process_file_wrapper, [(file, summary) for file in files])

    for result in results:
        if result:
            register_name, year, data = result
            if register_name not in summary:
                summary[register_name] = {}
            summary[register_name][year or register_name] = data


def process_file_wrapper(
    args: tuple[Path, dict[str, Any]],
) -> tuple[str, str, dict[str, Any]] | None:
    file_path, summary = args
    return process_file(file_path, summary)


def save_summary(summary: dict[str, Any], output_file: Path) -> None:
    with output_file.open("w") as f:
        ujson.dump(summary, f, indent=2)
    logger.info(f"Summary updated in {output_file}")


def print_summary_table(summary: dict[str, Any]) -> Panel:
    table = Table(
        title="Processing Summary", show_header=True, header_style="bold magenta"
    )
    table.add_column("Register", style="cyan", no_wrap=True)
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
                f"{data['num_rows']:,}",
                str(data["num_columns"]),
            )

    return Panel(table, expand=False, border_style="blue")


def process_files_with_progress(
    files: list[Path], summary: dict[str, Any], num_processes: int | None = None
) -> None:
    progress = Progress(
        SpinnerColumn(),
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TextColumn("[cyan]{task.completed}/{task.total}"),
        console=console,
        transient=True,
    )

    overall_task = progress.add_task("[green]Overall Progress", total=len(files))
    file_task = progress.add_task("[yellow]Current File", total=1, visible=False)

    with Live(progress, console=console, refresh_per_second=10) as live:
        with multiprocessing.Pool(processes=num_processes) as pool:
            for result in pool.imap_unordered(
                process_file_wrapper, [(file, summary) for file in files]
            ):
                if result:
                    register_name, year, data = result
                    if register_name not in summary:
                        summary[register_name] = {}
                    summary[register_name][year or register_name] = data

                progress.update(overall_task, advance=1)
                progress.update(file_task, completed=1, refresh=True)

                # Update the live display with current progress
                live.update(progress)


def run_convert():
    parser = argparse.ArgumentParser(
        description="Convert CSV/Parquet files to Parquet and generate summary."
    )
    parser.add_argument("input_directory", type=str, help="Path to the input directory")
    parser.add_argument(
        "--processes",
        type=int,
        default=4,
        help="Number of processes to use for parallel processing",
    )
    args = parser.parse_args()

    main(Path(args.input_directory), args.processes)


def main(input_directory: Path, num_processes: int | None = None) -> None:
    try:
        console.print(
            Panel(
                Text("Starting file conversion and processing", style="bold green"),
                expand=False,
            )
        )

        files = list(input_directory.rglob("*.parquet")) + list(
            input_directory.rglob("*.csv")
        )
        summary: dict[str, dict[str, Any]] = {}

        process_files_with_progress(files, summary, num_processes)

        console.print(print_summary_table(summary))

        console.print(
            Panel(Text("Processing complete!", style="bold green"), expand=False)
        )
        console.print(f"[bold blue]Total registers processed: {len(summary)}")
        console.print("[bold blue]Summary saved to: register_summary.json")
        console.print(
            f"[bold blue]Parquet files saved to: {OUTPUT_DIRECTORY}/registers"
        )
    except Exception as e:
        console.print(
            Panel(
                Text(f"An unexpected error occurred: {e}", style="bold red"),
                expand=False,
            )
        )
        logger.exception("Detailed error information:")


if __name__ == "__main__":
    run_convert()
