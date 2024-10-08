from pathlib import Path

import polars as pl

FAM_OUT = Path("data/01_family/cohort.parquet")


def parse_dates(col_name: str) -> pl.Expr:
    return pl.coalesce(
        # Prioritize formats with '/' separator
        pl.col(col_name).str.strptime(pl.Date, "%Y/%m/%d", strict=False),
        pl.col(col_name).str.strptime(pl.Date, "%d/%m/%Y", strict=False),
        pl.col(col_name).str.strptime(pl.Date, "%m/%d/%Y", strict=False),
        pl.col(col_name).str.strptime(pl.Date, "%Y/%m/%d %H:%M:%S", strict=False),
        pl.col(col_name).str.strptime(pl.Date, "%m/%d/%y", strict=False),
        # Then formats with '-' separator
        pl.col(col_name).str.strptime(pl.Date, "%Y-%m-%d", strict=False),
        pl.col(col_name).str.strptime(pl.Date, "%d-%m-%Y", strict=False),
        pl.col(col_name).str.strptime(pl.Date, "%m-%d-%Y", strict=False),
        pl.col(col_name).str.strptime(pl.Date, "%Y-%m-%d %H:%M:%S", strict=False),
        # Locale's appropriate date and time representation
        pl.col(col_name).str.strptime(pl.Date, "%c", strict=False),
    )


# Read all bef parquet files
bef_files = "directory/with/bef/files/*.parquet"
bef = pl.scan_parquet(bef_files, allow_missing_columns=True).with_columns(
    [parse_dates("FOED_DAG").alias("FOED_DAG_PARSED")]
)


# Process children
children = bef.filter(
    (pl.col("FOED_DAG_PARSED").dt.year() >= 1995)
    & (pl.col("FOED_DAG_PARSED").dt.year() <= 2020)
).select(["PNR", "FOED_DAG_PARSED", "FAR_ID", "MOR_ID", "FAMILIE_ID"])

# Get unique children
unique_children = (
    children.group_by("PNR")
    .agg(
        [
            pl.col("FOED_DAG_PARSED").first(),
            pl.col("FAR_ID").first(),
            pl.col("MOR_ID").first(),
            pl.col("FAMILIE_ID").first(),
        ]
    )
    .collect()
)

# Process parents
parents = (
    bef.select(["PNR", "FOED_DAG_PARSED"])
    .group_by("PNR")
    .agg(
        [
            pl.col("FOED_DAG_PARSED").first(),
        ]
    )
    .collect()
)

# Join children with father and mother
family = unique_children.join(
    parents.rename({"PNR": "FAR_ID", "FOED_DAG_PARSED": "FAR_FDAG"}),
    on="FAR_ID",
    how="left",
)

family = family.join(
    parents.rename({"PNR": "MOR_ID", "FOED_DAG_PARSED": "MOR_FDAG"}),
    on="MOR_ID",
    how="left",
)

# Select and arrange final columns in desired order
family = family.select(
    ["PNR", "FOED_DAG_PARSED", "FAR_ID", "FAR_FDAG", "MOR_ID", "MOR_FDAG", "FAMILIE_ID"]
)

# Print output to terminal
print(family)

# Write result into parquet file
family.write_parquet(FAM_OUT / "family.parquet")
