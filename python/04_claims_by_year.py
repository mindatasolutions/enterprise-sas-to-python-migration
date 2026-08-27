"""
Claims by year.

Python equivalent of:
sas/04_claims_by_year.sas
"""

import pandas as pd
import argparse

from generator.config import Config
from generator.logger import get_logger


logger = get_logger(__name__)


def create_claims_by_year(year: int) -> pd.DataFrame:
    """
    Create a claims dataset for a specified year.

    Parameters
    ----------
    year : int
        Claim year to filter.

    Returns
    -------
    pd.DataFrame
        Claims for the requested year.
    """

    logger.info(
        "Creating claims dataset for year %s",
        year
    )

    # ---------------------------------------------------------
    # Read source data
    # ---------------------------------------------------------

    claims = pd.read_csv(
        Config.RAW_DATA / "claims.csv"
    )

    # ---------------------------------------------------------
    # Convert claim date
    # ---------------------------------------------------------

    claims["claim_date"] = pd.to_datetime(
        claims["claim_date"]
    )

    # ---------------------------------------------------------
    # Filter by year
    # ---------------------------------------------------------

    result = claims[
        claims["claim_date"].dt.year == year
    ].copy()

    # ---------------------------------------------------------
    # Select columns equivalent to SAS SELECT
    # ---------------------------------------------------------

    result = result[
        [
            "claim_id",
            "patient_id",
            "provider_id",
            "claim_date",
            "claim_status",
            "billed_amount",
            "paid_amount",
        ]
    ]

    # ---------------------------------------------------------
    # Output
    # ---------------------------------------------------------

    output_file = (
        Config.PROCESSED_DATA
        / f"claims_{year}.csv"
    )

    result.to_csv(
        output_file,
        index=False
    )

    logger.info(
        "Created %s",
        output_file
    )

    return result


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Create claims dataset for a specified year."
    )

    parser.add_argument(
        "year",
        type=int,
        help="Claim year to process"
    )

    args = parser.parse_args()

    create_claims_by_year(args.year)
