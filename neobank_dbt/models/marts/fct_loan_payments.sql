{{ config(materialized='table') }}

select
    payment_id,
    client_id,
    payment_date,
    amount,
    loan_type,
    status
from {{ ref('stg_loan_payments') }}