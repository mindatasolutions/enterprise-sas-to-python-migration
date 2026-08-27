"""
Create provider-level claim summary.

Python equivalent of:
sas/02_provider_claim_summary.sas
"""

import pandas as pd

from generator.config import Config
from generator.logger import get_logger


logger = get_logger(__name__)


def create_provider_claim_summary():

    logger.info("Loading claims data...")

    claims = pd.read_csv(
        Config.RAW_DATA / "claims.csv"
    )

    logger.info(
        "Claims loaded: %s",
        len(claims)
    )

    # ---------------------------------------------------------
    # Convert date
    # ---------------------------------------------------------

    claims["claim_date"] = pd.to_datetime(
        claims["claim_date"]
    )

    # ---------------------------------------------------------
    # Filter claims
    # ---------------------------------------------------------

    claims = claims[
        claims["claim_date"].between(
            "2024-01-01",
            "2025-12-31"
        )
    ].copy()

    logger.info(
        "Claims after date filter: %s",
        len(claims)
    )

    # ---------------------------------------------------------
    # Conditional flags
    # ---------------------------------------------------------

    claims["paid_claim_flag"] = (
        claims["claim_status"] == "Paid"
    ).astype(int)

    claims["denied_claim_flag"] = (
        claims["claim_status"] == "Denied"
    ).astype(int)

    # ---------------------------------------------------------
    # Group and aggregate
    # ---------------------------------------------------------

    summary = (
        claims
        .groupby("provider_id")
        .agg(
            claim_count=(
                "claim_id",
                "count"
            ),

            total_billed=(
                "billed_amount",
                "sum"
            ),

            total_paid=(
                "paid_amount",
                "sum"
            ),

            average_paid=(
                "paid_amount",
                "mean"
            ),

            paid_claim_count=(
                "paid_claim_flag",
                "sum"
            ),

            denied_claim_count=(
                "denied_claim_flag",
                "sum"
            ),

            first_claim_date=(
                "claim_date",
                "min"
            ),

            last_claim_date=(
                "claim_date",
                "max"
            ),
        )
        .reset_index()
    )

    # ---------------------------------------------------------
    # Performance classification
    # ---------------------------------------------------------

    summary["performance_category"] = "Low"

    summary.loc[
        summary["total_paid"] >= 250_000,
        "performance_category"
    ] = "Medium"

    summary.loc[
        summary["total_paid"] >= 500_000,
        "performance_category"
    ] = "High"

    # ---------------------------------------------------------
    # Output
    # ---------------------------------------------------------

    output_file = (
        Config.PROCESSED_DATA
        / "provider_claim_summary.csv"
    )

    summary.to_csv(
        output_file,
        index=False
    )

    logger.info(
        "Created %s",
        output_file
    )

    logger.info(
        "Provider summary rows: %s",
        len(summary)
    )

    return summary


if __name__ == "__main__":
    create_provider_claim_summary()
