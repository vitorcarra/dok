{{ config(
    materialized='table',
    schema='data',
    alias='legislaturas_cleaned'
) }}

SELECT
    string_field_0 as id_legislatura,
   string_field_1 as sigla_casa,
   string_field_2 as num_legislatura,
   string_field_3 as data_inicio,
   string_field_4 as data_fim
FROM {{ source('data', 'legislaturas') }}