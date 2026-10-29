with source as (
    select * from {{ source('raw_neobank', 'loan_payments') }}
)

select
    payment_id,
    client_id,
    cast(payment_date as timestamp) as payment_date,
    amount,
    loan_type,
    status
from source