"""
Patient data generator.
"""

from datetime import datetime
import pandas as pd

from generator.config import Config
from generator.fake_data import fake
from generator.logger import get_logger
from generator.utils import random_gender, random_date


logger = get_logger(__name__)


class PatientGenerator:
    """
    Generate synthetic patient data.
    """

    def __init__(self):

        self.patient_count = Config.PATIENT_COUNT

    def generate(self) -> pd.DataFrame:

        logger.info("Generating %s patients...", self.patient_count)

        records = []

        for i in range(1, self.patient_count + 1):

            first = fake.first_name()

            last = fake.last_name()

            dob = random_date(
                datetime(1940, 1, 1),
                datetime(2023, 12, 31)
            )

            records.append(
                {
                    "patient_id": f"P{i:06d}",
                    "first_name": first,
                    "last_name": last,
                    "date_of_birth": dob.date(),
                    "gender": random_gender(),
                    "phone": fake.phone_number(),
                    "email": fake.email(),
                    "street": fake.street_address(),
                    "city": fake.city(),
                    "state": fake.state_abbr(),
                    "zip_code": fake.postcode(),
                    "registration_date": random_date(
                        datetime(2022, 1, 1),
                        datetime(2025, 12, 31)
                    ).date()
                }
            )

        df = pd.DataFrame(records)

        output_file = Config.RAW_DATA / "patients.csv"

        df.to_csv(output_file, index=False)

        logger.info(
            "Created %s",
            output_file
        )

        return df
