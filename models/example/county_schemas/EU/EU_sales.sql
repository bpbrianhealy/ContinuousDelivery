

{{ config(
    schema='EU'
) }}

with EU_SALES as (
   select 'EU' as Country,
          'South' as Region
)

select *
from EU_SALES
