# cdef-utils

cdef-utils is a Python package designed to convert CSV and Parquet files to a standardized Parquet format, specifically tailored for processing register data. It provides utilities for batch processing files, generating summaries, and handling various encoding issues.

## Features

- Convert CSV and Parquet files to a standardized Parquet format
- Automatic encoding detection for CSV files
- Batch processing of multiple files
- Generation of summary reports
- Progress tracking and resumable processing
- Rich console output with logging

## Installation

To install cdef-utils, you can use pip:

```
pip install cdef-utils
```

## Usage

You can use cdef-utils as a command-line tool:

```
python -m cdef_utils /path/to/input/directory --summary_file output_summary.json
```

### Arguments

- `input_directory`: Path to the directory containing CSV and Parquet files to process
- `--summary_file`: (Optional) Path to save the summary JSON file (default: "register_summary.json")

## Output

The script will:

1. Convert all CSV and Parquet files in the input directory to Parquet format
2. Save the converted files in a structured directory format under `/path/to/your/fixed/output/directory/registers`
3. Generate a summary JSON file with details about each processed register
4. Display a summary table in the console
5. Log processing details and any errors

## Requirements

- Python 3.7+
- polars
- rich

## Configuration

- The `OUTPUT_DIRECTORY` is set to `/path/to/your/fixed/output/directory` in the script. Modify this path as needed.
- Logging is configured to save logs in a `logs` directory in the current working directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
