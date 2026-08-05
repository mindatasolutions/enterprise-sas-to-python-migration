# from generator.config import Config
# from generator.logger import get_logger

# logger = get_logger(__name__)


# def main():

#     Config.create_directories()
#     # print(Config.LOGS)
#     logger.info("=" * 70)
#     logger.info("Enterprise SAS → Python Migration")
#     logger.info("=" * 70)

#     logger.info("Project Root : %s", Config.ROOT)
#     logger.info("Raw Data     : %s", Config.RAW_DATA)
#     logger.info("Processed    : %s", Config.PROCESSED_DATA)
#     logger.info("Output       : %s", Config.OUTPUT)

#     logger.info("Application started successfully.")


# if __name__ == "__main__":
#     main()

from datetime import datetime

from generator.logger import get_logger
from generator.utils import (
    random_date,
    random_gender,
    random_phone,
    random_email,
    random_zip,
)

logger = get_logger(__name__)


def main():

    logger.info("Testing utility functions")

    logger.info(
        "Random DOB: %s",
        random_date(
            datetime(1950, 1, 1),
            datetime(2020, 12, 31)
        )
    )

    logger.info(
        "Gender: %s",
        random_gender()
    )

    logger.info(
        "Phone: %s",
        random_phone()
    )

    logger.info(
        "Email: %s",
        random_email(
            "John",
            "Smith"
        )
    )

    logger.info(
        "ZIP: %s",
        random_zip()
    )


if __name__ == "__main__":
    main()