/*=============================================================
  Program: 01_claim_detail.sas
  Purpose: Create claim detail dataset
=============================================================*/

libname raw "data/raw";
libname out "data/processed";

proc sql;

    create table out.claim_detail as

    select
        c.claim_id,
        c.patient_id,
        c.provider_id,
        c.claim_date,

        /* Patient information */
        p.first_name as patient_first_name,
        p.last_name as patient_last_name,
        p.gender,
        p.date_of_birth,

        /* Provider information */
        pr.first_name as provider_first_name,
        pr.last_name as provider_last_name,
        pr.specialty,
        pr.organization,

        /* Claim information */
        c.diagnosis_code,
        c.procedure_code,
        c.billed_amount,
        c.paid_amount,
        c.claim_status,

        /* Derived fields */
        c.billed_amount - c.paid_amount
            as patient_responsibility,

        c.paid_amount / c.billed_amount
            as payment_ratio,

        year(c.claim_date)
            as claim_year

    from raw.claims as c

    left join raw.patients as p
        on c.patient_id = p.patient_id

    left join raw.providers as pr
        on c.provider_id = pr.provider_id

    ;

quit;
