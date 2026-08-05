"""
Reusable utility functions.

Shared by all generators.
"""

from datetime import datetime, timedelta
import random
import string


def random_date(start: datetime,
                end: datetime) -> datetime:
    """
    Return a random datetime between start and end.
    """

    delta = end - start

    random_days = random.randint(0, delta.days)

    return start + timedelta(days=random_days)


def random_gender() -> str:
    """
    Return random gender.
    """

    return random.choice(["M", "F"])


def random_phone() -> str:
    """
    Return phone number.
    """

    area = random.randint(200, 999)

    prefix = random.randint(100, 999)

    number = random.randint(1000, 9999)

    return f"{area}-{prefix}-{number}"


def random_email(first: str,
                 last: str) -> str:
    """
    Generate email.
    """

    domains = [
        "gmail.com",
        "outlook.com",
        "yahoo.com",
        "health.org"
    ]

    return (
        f"{first.lower()}."
        f"{last.lower()}"
        f"{random.randint(1,999)}"
        f"@{random.choice(domains)}"
    )


def random_zip() -> str:
    """
    Return ZIP code.
    """

    return str(random.randint(10000, 99999))


def random_string(length=8) -> str:
    """
    Return random text.
    """

    chars = string.ascii_uppercase

    return "".join(
        random.choice(chars)
        for _ in range(length)
    )
