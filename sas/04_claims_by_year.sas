/*
  Program: 04_claims_by_year.sas

  Purpose:
  Demonstrate migration of a parameterized SAS macro
  to a reusable Python function.
*/

libname raw "data/raw";
libname out "data/processed";


%macro create_claims_by_year(year);

    proc sql;

        create table out.claims_&year as

        select
            claim_id,
            patient_id,
            provider_id,
            claim_date,
            claim_status,
            billed_amount,
            paid_amount

        from raw.claims

        where year(claim_date) = &year;

    quit;

%mend;


/* Execute the macro */

%create_claims_by_year(2025);
