"""
Claim enrichment.

Python equivalent of:
sas/03_claim_enrichment.sas
"""

import pandas as pd

from generator.config import Config
from generator.logger import get_logger


logger = get_logger(__name__)


def create_claim_enriched():

    logger.info("Loading claims data...")

    claims = pd.read_csv(
        Config.RAW_DATA / "claims.csv"
    )

    logger.info(
        "Claims loaded: %s",
        len(claims)
    )

    # ---------------------------------------------------------
    # Convert claim date
    # ---------------------------------------------------------

    claims["claim_date"] = pd.to_datetime(
        claims["claim_date"]
    )

    # ---------------------------------------------------------
    # Extract claim year
    # ---------------------------------------------------------

    claims["claim_year"] = (
        claims["claim_date"].dt.year
    )

    # ---------------------------------------------------------
    # Calculate payment ratio
    # ---------------------------------------------------------

    claims["payment_ratio"] = 0.0

    billed_positive = (
        claims["billed_amount"] > 0
    )

    claims.loc[
        billed_positive,
        "payment_ratio"
    ] = (
        claims.loc[
            billed_positive,
            "paid_amount"
        ]
        /
        claims.loc[
            billed_positive,
            "billed_amount"
        ]
    )

    # ---------------------------------------------------------
    # Classify claim
    # ---------------------------------------------------------

    claims["claim_category"] = "Other Claim"

    claims.loc[
        claims["claim_status"] == "Paid",
        "claim_category"
    ] = "Paid Claim"

    claims.loc[
        claims["claim_status"] == "Denied",
        "claim_category"
    ] = "Denied Claim"

    # ---------------------------------------------------------
    # High-value claim indicator
    # ---------------------------------------------------------

    claims["high_value_flag"] = (
        claims["billed_amount"] >= 5000
    ).astype(int)

    # ---------------------------------------------------------
    # Save output
    # ---------------------------------------------------------

    output_file = (
        Config.PROCESSED_DATA
        / "claim_enriched.csv"
    )

    claims.to_csv(
        output_file,
        index=False
    )

    logger.info(
        "Created %s",
        output_file
    )

    return claims


if __name__ == "__main__":
    create_claim_enriched()
