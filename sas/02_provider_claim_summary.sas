/*=============================================================
  Program: 02_provider_claim_summary.sas
  Purpose: Create provider-level claim summary
=============================================================*/

libname raw "data/raw";
libname out "data/processed";

proc sql;

    create table out.provider_claim_summary as

    select
        provider_id,

        /* Number of claims */
        count(*) as claim_count,

        /* Financial totals */
        sum(billed_amount) as total_billed format=12.2,

        sum(paid_amount) as total_paid format=12.2,

        mean(paid_amount) as average_paid format=12.2,

        /* Conditional counts */
        sum(
            case
                when claim_status = "Paid"
                then 1
                else 0
            end
        ) as paid_claim_count,

        sum(
            case
                when claim_status = "Denied"
                then 1
                else 0
            end
        ) as denied_claim_count,

        /* Date information */
        min(claim_date) as first_claim_date format=date9.,

        max(claim_date) as last_claim_date format=date9.,

        /* Performance classification */
        case
            when sum(paid_amount) >= 500000
                then "High"

            when sum(paid_amount) >= 250000
                then "Medium"

            else "Low"
        end as performance_category length=10

    from raw.claims

    where claim_date between
        "01JAN2024"d and
        "31DEC2025"d

    group by provider_id

    ;

quit;
