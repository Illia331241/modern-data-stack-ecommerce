with source as (
    select * from {{ source('raw_neobank', 'clients') }}
),

cleaned as (
    select
        client_id,
        full_name,
        coalesce(email, 'unknown@example.com') as email,
        phone,
        city,
        cast(registration_date as date) as registration_date,
        branch_id,
        row_number() over (partition by client_id order by registration_date) as rn
    from source
)

select
    client_id,
    full_name,
    email,
    phone,
    city,
    registration_date,
    branch_id
from cleaned
where rn = 1