import re
from pathlib import Path

import polars as pl

# Constants
DATA_DIR = Path("E:/workdata/708245/data/register")
COHORT_FILE = Path("data/03_lpr/cohort.parquet")
OUTPUT_FILE = Path("data/04_covariates/cohort.parquet")


def read_cohort_data():
    return pl.read_parquet(COHORT_FILE)


def extract_year_from_filename(filename, dataset_type):
    if dataset_type == "bef":
        match = re.search(r"(\d{4})(\d{2})", filename.stem)
        if match:
            year, month = match.groups()
            return int(year)
    else:
        match = re.search(r"\d{4}", filename.stem)
        if match:
            return int(match.group())
    return None


def process_bef_data(cohort_data):
    bef_files = DATA_DIR.glob("bef/*.parquet")
    bef_data = pl.concat(
        [
            pl.read_parquet(f).with_columns(
                pl.lit(extract_year_from_filename(f, "bef")).alias("AAR")
            )
            for f in bef_files
        ]
    )

    return (
        bef_data.filter(pl.col("PNR").is_in(cohort_data["PNR"]))
        .group_by("PNR")
        .agg(
            [
                pl.col("ANTPERSH").alias("family_size").last(),
                pl.col("KOM").alias("geographical_location").last(),
                pl.col("IE_TYPE").alias("immigrant_background").first(),
                (pl.col("FAR_ID") == pl.col("AEGTE_ID"))
                .alias("parents_living_together")
                .first(),
            ]
        )
    )


def process_ind_data(cohort_data):
    ind_files = DATA_DIR.glob("ind/*.parquet")
    ind_data = pl.concat(
        [
            pl.read_parquet(f).with_columns(
                pl.lit(extract_year_from_filename(f, "ind")).alias("AAR")
            )
            for f in ind_files
        ]
    )

    return (
        ind_data.filter(pl.col("PNR").is_in(cohort_data["PNR"]))
        .filter(pl.col("AAR") >= pl.col("pre_exposure_start").dt.year() - 1)
        .filter(pl.col("AAR") < pl.col("pre_exposure_start").dt.year())
        .group_by("PNR")
        .agg(pl.col("PERINDK").mean().alias("pre_exposure_income"))
    )


def process_akm_data(cohort_data):
    akm_files = DATA_DIR.glob("akm/*.parquet")
    akm_data = pl.concat(
        [
            pl.read_parquet(f).with_columns(
                pl.lit(extract_year_from_filename(f, "akm")).alias("AAR")
            )
            for f in akm_files
        ]
    )

    return (
        akm_data.filter(pl.col("PNR").is_in(cohort_data["PNR"]))
        .filter(pl.col("AAR") == pl.col("pre_exposure_start").dt.year() - 1)
        .group_by("PNR")
        .agg(pl.col("SOCIO13").alias("pre_exposure_employment_status").last())
    )


def process_idan_data(cohort_data):
    idan_files = DATA_DIR.glob("idan/*.parquet")
    idan_data = pl.concat(
        [
            pl.read_parquet(f).with_columns(
                pl.lit(extract_year_from_filename(f, "idan")).alias("AAR")
            )
            for f in idan_files
        ]
    )

    return (
        idan_data.filter(pl.col("PNR").is_in(cohort_data["PNR"]))
        .filter(pl.col("AAR") == pl.col("pre_exposure_start").dt.year() - 1)
        .group_by("PNR")
        .agg(pl.col("STILL").alias("pre_diagnosis_job_situation").last())
    )


def main():
    cohort_data = read_cohort_data()
    bef_data = process_bef_data(cohort_data)
    ind_data = process_ind_data(cohort_data)
    akm_data = process_akm_data(cohort_data)
    idan_data = process_idan_data(cohort_data)

    # Join all data
    final_data = (
        cohort_data.join(bef_data, on="PNR", how="left")
        .join(ind_data, on="PNR", how="left")
        .join(akm_data, on="PNR", how="left")
        .join(idan_data, on="PNR", how="left")
    )

    # Write output
    final_data.write_parquet(OUTPUT_FILE)
    print(f"Data written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
