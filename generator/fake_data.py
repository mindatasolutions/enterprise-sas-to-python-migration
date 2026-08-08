"""
Reusable Faker instance.
"""

from faker import Faker

fake = Faker("en_US")

# Make generated data reproducible
Faker.seed(12345)
