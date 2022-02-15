

{% if target.name == 'test' %}
{{ config(
    schema='marketing',
    database= 'DGTL_TST'
) }}
{% endif %}

with EU_SALES as (

   select 'EU' as Area
    , 'North' as Region
    , 'sweden' as Country_name
)

select *
from EU_SALES
