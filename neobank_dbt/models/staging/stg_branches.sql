with source as (
    select * from {{ source('raw_neobank', 'branches') }}
)

select
    branch_id,
    branch_name,
    city,
    region
from source