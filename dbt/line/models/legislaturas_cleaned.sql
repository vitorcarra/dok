{{ config(
    materialized='table',
    schema='data',
    alias='legislaturas_cleaned'
) }}

SELECT *
FROM {{ source('data', 'legislaturas') }}