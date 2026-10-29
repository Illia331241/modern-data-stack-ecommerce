with source as (
    select * from {{ source('raw_neobank', 'transfers') }}
)

select
    transfer_id,
    from_account_id,
    to_account_id,
    amount,
    cast(transfer_date as timestamp) as transfer_date,
    status,
    coalesce(description, 'no description') as description
from source