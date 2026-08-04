"""
Project configuration.

This module centralizes project paths and constants so they are not
hardcoded throughout the project.
"""

from pathlib import Path


class Config:
    """Project configuration."""

    # Project root
    ROOT = Path(__file__).resolve().parent.parent

    # Data folders
    DATA = ROOT / "data"

    RAW_DATA = DATA / "raw"

    PROCESSED_DATA = DATA / "processed"

    OUTPUT = DATA / "output"

    LOGS = ROOT / "logs"

    REPORTS = ROOT / "reports"

    DOCS = ROOT / "docs"

    TESTS = ROOT / "tests"

    RANDOM_SEED = 12345

    PATIENT_COUNT = 100_000

    PROVIDER_COUNT = 5_000

    CLAIM_COUNT = 1_000_000
