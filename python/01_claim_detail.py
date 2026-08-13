"""
Create claim detail dataset.

Python equivalent of:
sas/01_claim_detail.sas
"""

import pandas as pd

from generator.config import Config
from generator.logger import get_logger


logger = get_logger(__name__)


def create_claim_detail():

    logger.info("Loading source datasets...")

    patients = pd.read_csv(
        Config.RAW_DATA / "patients.csv"
    )

    providers = pd.read_csv(
        Config.RAW_DATA / "providers.csv"
    )

    claims = pd.read_csv(
        Config.RAW_DATA / "claims.csv"
    )

    logger.info("Patients loaded: %s", len(patients))
    logger.info("Providers loaded: %s", len(providers))
    logger.info("Claims loaded: %s", len(claims))

    # ---------------------------------------------------------
    # Patient columns
    # ---------------------------------------------------------

    patient_columns = [
        "patient_id",
        "first_name",
        "last_name",
        "gender",
        "date_of_birth",
    ]

    patients = patients[patient_columns].rename(
        columns={
            "first_name": "patient_first_name",
            "last_name": "patient_last_name",
        }
    )

    # ---------------------------------------------------------
    # Provider columns
    # ---------------------------------------------------------

    provider_columns = [
        "provider_id",
        "first_name",
        "last_name",
        "specialty",
        "organization",
    ]

    providers = providers[provider_columns].rename(
        columns={
            "first_name": "provider_first_name",
            "last_name": "provider_last_name",
        }
    )

    # ---------------------------------------------------------
    # Join claims to patients
    # ---------------------------------------------------------

    claim_detail = claims.merge(
        patients,
        on="patient_id",
        how="left",
        validate="many_to_one",
    )

    # ---------------------------------------------------------
    # Join to providers
    # ---------------------------------------------------------

    claim_detail = claim_detail.merge(
        providers,
        on="provider_id",
        how="left",
        validate="many_to_one",
    )

    # ---------------------------------------------------------
    # Derived fields
    # ---------------------------------------------------------

    claim_detail["claim_date"] = pd.to_datetime(
        claim_detail["claim_date"]
    )

    claim_detail["patient_responsibility"] = (
        claim_detail["billed_amount"]
        - claim_detail["paid_amount"]
    )

    claim_detail["payment_ratio"] = (
        claim_detail["paid_amount"]
        / claim_detail["billed_amount"]
    )

    claim_detail["claim_year"] = (
        claim_detail["claim_date"].dt.year
    )

    # ---------------------------------------------------------
    # Output
    # ---------------------------------------------------------

    output_file = (
        Config.PROCESSED_DATA
        / "claim_detail.csv"
    )

    claim_detail.to_csv(
        output_file,
        index=False,
    )

    logger.info(
        "Created %s",
        output_file,
    )

    logger.info(
        "Claim detail rows: %s",
        len(claim_detail),
    )

    return claim_detail


if __name__ == "__main__":
    create_claim_detail()
