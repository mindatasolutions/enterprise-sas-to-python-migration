"""
Reusable SAS vs Python reconciliation framework.
"""

import argparse
from pathlib import Path

import pandas as pd


def reconcile_outputs(
    sas_file: Path,
    python_file: Path,
    key_column: str,
) -> None:
    """
    Compare SAS and Python output datasets.

    Parameters
    ----------
    sas_file : Path
        SAS output file.

    python_file : Path
        Python output file.

    key_column : str
        Unique key used to align records.
    """

    print("=" * 70)
    print("SAS vs PYTHON RECONCILIATION")
    print("=" * 70)

    # ---------------------------------------------------------
    # Load data
    # ---------------------------------------------------------

    sas = pd.read_csv(sas_file)
    python = pd.read_csv(python_file)

    print()
    print("Files:")
    print(f"SAS    : {sas_file}")
    print(f"Python : {python_file}")

    print()
    print("Dataset sizes:")
    print(f"SAS rows    : {len(sas):,}")
    print(f"Python rows : {len(python):,}")

    # ---------------------------------------------------------
    # 1. Row count
    # ---------------------------------------------------------

    if len(sas) != len(python):
        raise AssertionError(
            "Row counts do not match"
        )

    print("✓ Row count matched")

    # ---------------------------------------------------------
    # 2. Column structure
    # ---------------------------------------------------------

    if list(sas.columns) != list(python.columns):
        print()
        print("SAS columns:")
        print(list(sas.columns))

        print()
        print("Python columns:")
        print(list(python.columns))

        raise AssertionError(
            "Column structures do not match"
        )

    print("✓ Column structure matched")

    # ---------------------------------------------------------
    # 3. Key existence
    # ---------------------------------------------------------

    if key_column not in sas.columns:
        raise AssertionError(
            f"{key_column} not found in SAS output"
        )

    if key_column not in python.columns:
        raise AssertionError(
            f"{key_column} not found in Python output"
        )

    # ---------------------------------------------------------
    # 4. Key uniqueness
    # ---------------------------------------------------------

    if sas[key_column].duplicated().any():
        raise AssertionError(
            f"Duplicate {key_column} values in SAS output"
        )

    if python[key_column].duplicated().any():
        raise AssertionError(
            f"Duplicate {key_column} values in Python output"
        )

    print(
        f"✓ {key_column} uniqueness passed"
    )

    # ---------------------------------------------------------
    # 5. Key comparison
    # ---------------------------------------------------------

    sas_keys = set(sas[key_column])
    python_keys = set(python[key_column])

    sas_only = sas_keys - python_keys
    python_only = python_keys - sas_keys

    print(
        f"SAS-only keys    : {len(sas_only):,}"
    )

    print(
        f"Python-only keys : {len(python_only):,}"
    )

    if sas_only or python_only:
        raise AssertionError(
            "Key values do not match"
        )

    print("✓ Key values matched")

    # ---------------------------------------------------------
    # 6. Sort by key
    # ---------------------------------------------------------

    sas = sas.sort_values(
        key_column
    ).reset_index(drop=True)

    python = python.sort_values(
        key_column
    ).reset_index(drop=True)

    # ---------------------------------------------------------
    # 7. Compare values
    # ---------------------------------------------------------

    differences = []

    for column in sas.columns:

        if column == key_column:
            continue

        sas_series = sas[column]
        python_series = python[column]

        # Character columns
        if (
            sas_series.dtype == "object"
            or python_series.dtype == "object"
        ):

            sas_values = (
                sas_series
                .fillna("<NULL>")
                .astype(str)
            )

            python_values = (
                python_series
                .fillna("<NULL>")
                .astype(str)
            )

            mismatch = (
                sas_values != python_values
            )

        # Numeric columns
        elif (
            pd.api.types.is_numeric_dtype(
                sas_series
            )
            and pd.api.types.is_numeric_dtype(
                python_series
            )
        ):

            mismatch = ~(
                sas_series.eq(
                    python_series
                )
                | (
                    sas_series
                    .sub(python_series)
                    .abs()
                    < 1e-9
                )
                | (
                    sas_series.isna()
                    & python_series.isna()
                )
            )

        # Other data types
        else:

            mismatch = (
                sas_series != python_series
            )

            mismatch = (
                mismatch
                & ~(
                    sas_series.isna()
                    & python_series.isna()
                )
            )

        mismatch_count = int(
            mismatch.sum()
        )

        if mismatch_count > 0:

            differences.append(
                {
                    "column": column,
                    "differences": mismatch_count,
                }
            )

    # ---------------------------------------------------------
    # 8. Report differences
    # ---------------------------------------------------------

    if differences:

        print()
        print("✗ Data differences found:")

        for difference in differences:

            print(
                f"  {difference['column']}: "
                f"{difference['differences']:,}"
            )

        raise AssertionError(
            "SAS and Python output values do not match"
        )

    print("✓ All data values matched")

    print()
    print("=" * 70)
    print("RECONCILIATION PASSED")
    print("=" * 70)


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Compare SAS and Python datasets"
        )
    )

    parser.add_argument(
        "sas_file",
        help="Path to SAS output CSV",
    )

    parser.add_argument(
        "python_file",
        help="Path to Python output CSV",
    )

    parser.add_argument(
        "key_column",
        help="Unique key column",
    )

    args = parser.parse_args()

    reconcile_outputs(
        Path(args.sas_file),
        Path(args.python_file),
        args.key_column,
    )


if __name__ == "__main__":
    main()
