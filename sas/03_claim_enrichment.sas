/*=============================================================
  Program: 03_claim_enrichment.sas
  Purpose: Enrich claim-level data using a SAS DATA step
=============================================================*/

libname raw "data/raw";
libname out "data/processed";

data out.claim_enriched;

    set raw.claims;

    /*---------------------------------------------------------
      Extract year from claim date
    ---------------------------------------------------------*/

    claim_year = year(claim_date);

    /*---------------------------------------------------------
      Calculate payment ratio
    ---------------------------------------------------------*/

    if billed_amount > 0 then
        payment_ratio = paid_amount / billed_amount;
    else
        payment_ratio = 0;

    /*---------------------------------------------------------
      Classify claim
    ---------------------------------------------------------*/

    if claim_status = "Paid" then
        claim_category = "Paid Claim";

    else if claim_status = "Denied" then
        claim_category = "Denied Claim";

    else
        claim_category = "Other Claim";

    /*---------------------------------------------------------
      High-value claim indicator
    ---------------------------------------------------------*/

    if billed_amount >= 5000 then
        high_value_flag = 1;
    else
        high_value_flag = 0;

run;
