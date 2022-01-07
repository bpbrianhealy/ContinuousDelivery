

{{ config(
    schema='EU'
) }}

with EU_SALES as (

   select 'EU' as Country
    , 'North' as Region
    , 'sweden' as Country_name
)

select *
from EU_SALES
