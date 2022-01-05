

{{ config(
    schema='EU'
) }}

with EU_SALES as (
   select 'EU' as Country

)

select *
from EU_SALES
