"""
Project entry point.
"""

# from config import Config
from generator.config import Config

def main():

    print("=" * 60)

    print("Enterprise SAS -> Python Migration")

    print("=" * 60)

    print(f"Project Root : {Config.ROOT}")

    print(f"Raw Data     : {Config.RAW_DATA}")

    print(f"Output       : {Config.OUTPUT}")

    print()

    print("Configuration loaded successfully.")


if __name__ == "__main__":
    main()
