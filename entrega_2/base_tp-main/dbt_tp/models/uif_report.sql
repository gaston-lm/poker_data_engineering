{{ config(materialized='table') }}

SELECT DISTINCT 
    id_jugador, nombre, apellido
FROM 
    {{ ref('all_in_players') }}

UNION

SELECT DISTINCT 
    id_jugador, nombre, apellido
FROM 
    {{ ref('top_winners') }}