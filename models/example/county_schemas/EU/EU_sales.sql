{{ config(
    schema='marketing'
) }}

with EU_SALES as (

   select 'EU' as Area
    , 'North' as Region
    , 'sweden' as Country_name
)

select *
from EU_SALES
