{{ config(materialized='view') }}

SELECT
    a.id_jugador AS id_jugador_a,
    a.nombre AS nombre_jugador_a,
    a.apellido AS apellido_jugador_a,
    a.id_partido AS id_partido_a,
    a.mano_en_partido AS mano_en_partido_a,
    b.id_jugador AS id_jugador_b,
    b.nombre AS nombre_jugador_b,
    b.apellido AS apellido_jugador_b,
    t.id_jugador AS id_jugador_t,
    t.nombre AS nombre_jugador_t,
    t.apellido AS apellido_jugador_t,
    b.*,
    t.*
FROM 
    {{ ref('all_in_players') }} a
INNER JOIN 
    {{ ref('players_behavior') }} b ON a.id_jugador = b.id_jugador
INNER JOIN
    {{ ref('top_winners') }} t ON a.id_jugador = t.id_jugador