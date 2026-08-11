"""
Provider data generator.
"""

import pandas as pd

from generator.config import Config
from generator.fake_data import fake
from generator.logger import get_logger

logger = get_logger(__name__)


class ProviderGenerator:
    """
    Generate synthetic healthcare provider data.
    """

    def __init__(self):

        self.provider_count = Config.PROVIDER_COUNT

    def generate(self) -> pd.DataFrame:

        logger.info(
            "Generating %s providers...",
            self.provider_count
        )

        records = []

        specialties = [
            "Cardiology",
            "Dermatology",
            "Emergency Medicine",
            "Family Medicine",
            "Internal Medicine",
            "Neurology",
            "Oncology",
            "Orthopedics",
            "Pediatrics",
            "Psychiatry",
            "Radiology",
            "Surgery",
        ]

        provider_types = [
            "Physician",
            "Nurse Practitioner",
            "Physician Assistant",
        ]

        for i in range(1, self.provider_count + 1):

            records.append(
                {
                    "provider_id": f"PR{i:05d}",
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "provider_type": fake.random_element(
                        provider_types
                    ),
                    "specialty": fake.random_element(
                        specialties
                    ),
                    "organization": fake.company(),
                    "phone": fake.phone_number(),
                    "email": fake.email(),
                    "street": fake.street_address(),
                    "city": fake.city(),
                    "state": fake.state_abbr(),
                    "zip_code": fake.postcode(),
                }
            )

        df = pd.DataFrame(records)

        output_file = Config.RAW_DATA / "providers.csv"

        df.to_csv(
            output_file,
            index=False
        )

        logger.info(
            "Created %s",
            output_file
        )

        return df
