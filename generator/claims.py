"""
Claims data generator.
"""

import numpy as np
import pandas as pd

from generator.config import Config
from generator.logger import get_logger


logger = get_logger(__name__)


class ClaimsGenerator:
    """
    Generate synthetic healthcare claims data.
    """

    def __init__(self):

        self.claim_count = Config.CLAIM_COUNT

        self.rng = np.random.default_rng(
            Config.RANDOM_SEED
        )

    def generate(self) -> pd.DataFrame:

        logger.info(
            "Generating %s claims...",
            self.claim_count
        )

        # Generate claim IDs
        claim_ids = [
            f"C{i:08d}"
            for i in range(1, self.claim_count + 1)
        ]

        # Generate patient IDs
        patient_numbers = self.rng.integers(
            1,
            Config.PATIENT_COUNT + 1,
            size=self.claim_count
        )

        patient_ids = [
            f"P{i:06d}"
            for i in patient_numbers
        ]

        # Generate provider IDs
        provider_numbers = self.rng.integers(
            1,
            Config.PROVIDER_COUNT + 1,
            size=self.claim_count
        )

        provider_ids = [
            f"PR{i:05d}"
            for i in provider_numbers
        ]

        # Claim dates
        start_date = pd.Timestamp("2024-01-01")
        end_date = pd.Timestamp("2025-12-31")

        days = (
            end_date - start_date
        ).days

        claim_dates = (
            start_date
            + pd.to_timedelta(
                self.rng.integers(
                    0,
                    days + 1,
                    size=self.claim_count
                ),
                unit="D"
            )
        )

        # Diagnosis codes
        diagnosis_codes = self.rng.choice(
            [
                "I10",
                "E11.9",
                "J06.9",
                "M54.5",
                "E78.5",
                "K21.9",
                "F32.9",
                "J45.909",
                "N39.0",
                "G43.909",
            ],
            size=self.claim_count
        )

        # Procedure codes
        procedure_codes = self.rng.choice(
            [
                "99201",
                "99202",
                "99203",
                "99204",
                "99205",
                "99211",
                "99212",
                "99213",
                "99214",
                "99215",
            ],
            size=self.claim_count
        )

        # Financial amounts
        billed_amount = np.round(
            self.rng.uniform(
                50,
                5000,
                size=self.claim_count
            ),
            2
        )

        paid_amount = np.round(
            billed_amount
            * self.rng.uniform(
                0.40,
                0.90,
                size=self.claim_count
            ),
            2
        )

        # Claim status
        claim_status = self.rng.choice(
            [
                "Paid",
                "Denied",
                "Pending",
            ],
            size=self.claim_count,
            p=[
                0.75,
                0.15,
                0.10,
            ]
        )

        df = pd.DataFrame(
            {
                "claim_id": claim_ids,
                "patient_id": patient_ids,
                "provider_id": provider_ids,
                "claim_date": claim_dates,
                "diagnosis_code": diagnosis_codes,
                "procedure_code": procedure_codes,
                "billed_amount": billed_amount,
                "paid_amount": paid_amount,
                "claim_status": claim_status,
            }
        )

        output_file = Config.RAW_DATA / "claims.csv"

        df.to_csv(
            output_file,
            index=False
        )

        logger.info(
            "Created %s",
            output_file
        )

        return df
