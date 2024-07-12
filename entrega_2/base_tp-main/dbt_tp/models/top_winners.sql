{{ config(materialized='view') }}

WITH total_apostado_por_mano AS (
	SELECT jr.id_partido, jr.mano_en_partido, sum(jr.apuesta) AS total_apostado
	FROM {{source('poker','jugadoresenronda')}} jr
	GROUP BY jr.id_partido, jr.mano_en_partido
)

SELECT
	j.id_jugador, j.nombre, j.apellido, sum(t.total_apostado) AS total_ganado
FROM
	{{source('poker','jugadoresjuegancon')}} jjc
NATURAL JOIN
	{{source('poker','jugadores')}} j
INNER JOIN
	total_apostado_por_mano t ON t.id_partido = jjc.id_partido AND t.mano_en_partido = jjc.mano_en_partido 
INNER JOIN
    {{source('poker','partidos')}} p ON p.id_partido = jjc.id_partido
WHERE
    p.hora_inicio >= NOW() - INTERVAL '7 days'
GROUP BY 
	j.id_jugador, j.nombre, j.apellido, jjc.es_ganador
HAVING 
	jjc.es_ganador = TRUE
ORDER BY 
	sum(t.total_apostado) DESC
LIMIT 20