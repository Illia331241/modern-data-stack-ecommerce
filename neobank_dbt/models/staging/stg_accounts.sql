with source as (
    select * from {{ source('raw_neobank', 'accounts') }}
)

select
    account_id,
    client_id,
    account_number,
    account_type,
    balance,
    currency,
    cast(opened_date as date) as opened_date,
    is_active
from source