"""
Compare SAS and Python output datasets.
"""

import pandas as pd

from generator.config import Config


def reconcile_outputs(
    sas_file,
    python_file,
    key_column="claim_id",
):
    """
    Compare SAS and Python output datasets.
    """

    print("=" * 70)
    print("SAS vs PYTHON RECONCILIATION")
    print("=" * 70)

    sas = pd.read_csv(sas_file)
    python = pd.read_csv(python_file)

    print()
    print("Dataset sizes:")
    print(f"SAS rows    : {len(sas):,}")
    print(f"Python rows : {len(python):,}")

    # ---------------------------------------------------------
    # 1. Row count
    # ---------------------------------------------------------

    assert len(sas) == len(python), (
        "Row counts do not match"
    )

    print("✓ Row count matched")

    # ---------------------------------------------------------
    # 2. Column names
    # ---------------------------------------------------------

    sas_columns = list(sas.columns)
    python_columns = list(python.columns)

    assert sas_columns == python_columns, (
        "Column structures do not match"
    )

    print("✓ Column structure matched")

    # ---------------------------------------------------------
    # 3. Key uniqueness
    # ---------------------------------------------------------

    assert not sas[key_column].duplicated().any(), (
        f"Duplicate {key_column} values in SAS output"
    )

    assert not python[key_column].duplicated().any(), (
        f"Duplicate {key_column} values in Python output"
    )

    print(f"✓ {key_column} uniqueness passed")

    # ---------------------------------------------------------
    # 4. Key comparison
    # ---------------------------------------------------------

    sas_keys = set(sas[key_column])
    python_keys = set(python[key_column])

    sas_only = sas_keys - python_keys
    python_only = python_keys - sas_keys

    print(f"SAS-only keys    : {len(sas_only):,}")
    print(f"Python-only keys : {len(python_only):,}")

    assert len(sas_only) == 0, (
        "Keys exist in SAS but not Python"
    )

    assert len(python_only) == 0, (
        "Keys exist in Python but not SAS"
    )

    print("✓ Key values matched")

    # ---------------------------------------------------------
    # 5. Sort both datasets by key
    # ---------------------------------------------------------

    sas = sas.sort_values(
        key_column
    ).reset_index(drop=True)

    python = python.sort_values(
        key_column
    ).reset_index(drop=True)

    # ---------------------------------------------------------
    # 6. Compare individual columns
    # ---------------------------------------------------------

    differences = []

    for column in sas_columns:

        sas_series = sas[column]
        python_series = python[column]

        # Convert both sides to string for character comparison.
        # This avoids false differences caused by pandas dtypes.
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

            mismatch = sas_values != python_values

        else:

            # Numeric comparison with a small tolerance.
            if (
                pd.api.types.is_numeric_dtype(sas_series)
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

        mismatch_count = mismatch.sum()

        if mismatch_count > 0:

            differences.append(
                {
                    "column": column,
                    "differences": int(
                        mismatch_count
                    ),
                }
            )

    # ---------------------------------------------------------
    # 7. Report differences
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

    # ---------------------------------------------------------
    # Final result
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print("RECONCILIATION PASSED")
    print("=" * 70)


if __name__ == "__main__":

    sas_output = (
        Config.PROCESSED_DATA
        / "claim_detail_sas.csv"
    )

    python_output = (
        Config.PROCESSED_DATA
        / "claim_detail.csv"
    )

    reconcile_outputs(
        sas_output,
        python_output,
    )
