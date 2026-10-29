{{ config(materialized='table') }}

select
    transfer_id,
    from_account_id,
    to_account_id,
    amount,
    transfer_date,
    status,
    description
from {{ ref('stg_transfers') }}