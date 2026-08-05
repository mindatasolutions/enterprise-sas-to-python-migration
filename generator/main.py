from generator.config import Config
from generator.logger import get_logger

logger = get_logger(__name__)


def main():

    Config.create_directories()

    logger.info("=" * 70)
    logger.info("Enterprise SAS → Python Migration")
    logger.info("=" * 70)

    logger.info("Project Root : %s", Config.ROOT)
    logger.info("Raw Data     : %s", Config.RAW_DATA)
    logger.info("Processed    : %s", Config.PROCESSED_DATA)
    logger.info("Output       : %s", Config.OUTPUT)

    logger.info("Application started successfully.")


if __name__ == "__main__":
    main()