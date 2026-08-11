"""
Data quality validation for generated healthcare source data.
"""

from pathlib import Path

import pandas as pd

from generator.config import Config


def validate_raw_data() -> None:
    """
    Validate patients, providers, and claims source data.
    """

    print("=" * 70)
    print("RAW DATA QUALITY VALIDATION")
    print("=" * 70)

    patients_file = Config.RAW_DATA / "patients.csv"
    providers_file = Config.RAW_DATA / "providers.csv"
    claims_file = Config.RAW_DATA / "claims.csv"

    # ---------------------------------------------------------
    # 1. Check that source files exist
    # ---------------------------------------------------------

    files = {
        "patients": patients_file,
        "providers": providers_file,
        "claims": claims_file,
    }

    for name, file_path in files.items():

        if not file_path.exists():
            raise FileNotFoundError(
                f"{name} file not found: {file_path}"
            )

        print(f"✓ {name.capitalize()} file exists")

    # ---------------------------------------------------------
    # 2. Load source data
    # ---------------------------------------------------------

    patients = pd.read_csv(patients_file)
    providers = pd.read_csv(providers_file)
    claims = pd.read_csv(claims_file)

    print()
    print("Row counts:")
    print(f"Patients  : {len(patients):,}")
    print(f"Providers : {len(providers):,}")
    print(f"Claims    : {len(claims):,}")

    # ---------------------------------------------------------
    # 3. Validate expected row counts
    # ---------------------------------------------------------

    assert len(patients) == Config.PATIENT_COUNT, (
        f"Expected {Config.PATIENT_COUNT:,} patients, "
        f"found {len(patients):,}"
    )

    assert len(providers) == Config.PROVIDER_COUNT, (
        f"Expected {Config.PROVIDER_COUNT:,} providers, "
        f"found {len(providers):,}"
    )

    assert len(claims) == Config.CLAIM_COUNT, (
        f"Expected {Config.CLAIM_COUNT:,} claims, "
        f"found {len(claims):,}"
    )

    print()
    print("✓ Expected row counts passed")

    # ---------------------------------------------------------
    # 4. Primary-key uniqueness
    # ---------------------------------------------------------

    patient_duplicates = patients["patient_id"].duplicated().sum()

    provider_duplicates = providers["provider_id"].duplicated().sum()

    claim_duplicates = claims["claim_id"].duplicated().sum()

    print()
    print("Duplicate primary keys:")
    print(f"Patients  : {patient_duplicates:,}")
    print(f"Providers : {provider_duplicates:,}")
    print(f"Claims    : {claim_duplicates:,}")

    assert patient_duplicates == 0, (
        "Duplicate patient_id values found"
    )

    assert provider_duplicates == 0, (
        "Duplicate provider_id values found"
    )

    assert claim_duplicates == 0, (
        "Duplicate claim_id values found"
    )

    print("✓ Primary-key uniqueness passed")

    # ---------------------------------------------------------
    # 5. Missing values
    # ---------------------------------------------------------

    patient_missing = patients.isna().sum().sum()
    provider_missing = providers.isna().sum().sum()
    claim_missing = claims.isna().sum().sum()

    print()
    print("Missing values:")
    print(f"Patients  : {patient_missing:,}")
    print(f"Providers : {provider_missing:,}")
    print(f"Claims    : {claim_missing:,}")

    assert patient_missing == 0, (
        "Missing values found in patients"
    )

    assert provider_missing == 0, (
        "Missing values found in providers"
    )

    assert claim_missing == 0, (
        "Missing values found in claims"
    )

    print("✓ Missing-value validation passed")

    # ---------------------------------------------------------
    # 6. Referential integrity - patient
    # ---------------------------------------------------------

    patient_ids = set(
        patients["patient_id"]
    )

    invalid_patient_ids = (
        ~claims["patient_id"].isin(patient_ids)
    ).sum()

    print()
    print(
        f"Claims with invalid patient_id: "
        f"{invalid_patient_ids:,}"
    )

    assert invalid_patient_ids == 0, (
        "Claims contain invalid patient_id values"
    )

    print("✓ Patient referential integrity passed")

    # ---------------------------------------------------------
    # 7. Referential integrity - provider
    # ---------------------------------------------------------

    provider_ids = set(
        providers["provider_id"]
    )

    invalid_provider_ids = (
        ~claims["provider_id"].isin(provider_ids)
    ).sum()

    print(
        f"Claims with invalid provider_id: "
        f"{invalid_provider_ids:,}"
    )

    assert invalid_provider_ids == 0, (
        "Claims contain invalid provider_id values"
    )

    print("✓ Provider referential integrity passed")

    # ---------------------------------------------------------
    # 8. Claim status validation
    # ---------------------------------------------------------

    valid_statuses = {
        "Paid",
        "Denied",
        "Pending",
    }

    invalid_statuses = (
        ~claims["claim_status"].isin(valid_statuses)
    ).sum()

    print()
    print(
        f"Claims with invalid claim_status: "
        f"{invalid_statuses:,}"
    )

    assert invalid_statuses == 0, (
        "Invalid claim_status values found"
    )

    print("✓ Claim status validation passed")

    # ---------------------------------------------------------
    # 9. Financial validation
    # ---------------------------------------------------------

    invalid_amounts = (
        claims["paid_amount"] > claims["billed_amount"]
    ).sum()

    negative_billed = (
        claims["billed_amount"] < 0
    ).sum()

    negative_paid = (
        claims["paid_amount"] < 0
    ).sum()

    print()
    print(
        f"Claims where paid > billed: "
        f"{invalid_amounts:,}"
    )

    print(
        f"Negative billed amounts: "
        f"{negative_billed:,}"
    )

    print(
        f"Negative paid amounts: "
        f"{negative_paid:,}"
    )

    assert invalid_amounts == 0, (
        "Some claims have paid_amount greater than billed_amount"
    )

    assert negative_billed == 0, (
        "Negative billed_amount values found"
    )

    assert negative_paid == 0, (
        "Negative paid_amount values found"
    )

    print("✓ Financial validation passed")

    # ---------------------------------------------------------
    # 10. Date validation
    # ---------------------------------------------------------

    claims["claim_date"] = pd.to_datetime(
        claims["claim_date"],
        errors="coerce"
    )

    invalid_dates = claims["claim_date"].isna().sum()

    print()
    print(
        f"Invalid claim dates: {invalid_dates:,}"
    )

    assert invalid_dates == 0, (
        "Invalid claim_date values found"
    )

    print("✓ Date validation passed")

    # ---------------------------------------------------------
    # Final result
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print("DATA QUALITY VALIDATION PASSED")
    print("=" * 70)


if __name__ == "__main__":
    validate_raw_data()
