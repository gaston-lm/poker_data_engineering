{{ config(materialized='view') }}

WITH diferencias_jugadores AS (
	SELECT 
		jr.id_partido, 
		jr.mano_en_partido, 
		jr.id_jugador,
		jr.ronda_en_mano,
		jr.apuesta,
		jr.apuesta - lag(apuesta,1) OVER (
			PARTITION BY jr.id_partido, jr.mano_en_partido, jr.id_jugador 
			ORDER BY jr.ronda_en_mano 
		) AS diferencia_apuesta
	FROM {{source('poker','jugadoresenronda')}} jr
)

SELECT 
    dj.id_partido,
	dj.mano_en_partido, 
	dj.ronda_en_mano,
    j.id_jugador,
	j.nombre,
	j.apellido,
	dj.apuesta,
	CASE 
		WHEN dj.diferencia_apuesta <= 0 THEN 'se achicó'
		WHEN dj.diferencia_apuesta > 0 THEN 'se agrandó'
		ELSE 'primera apuesta'
	END AS comportamiento
FROM diferencias_jugadores dj
NATURAL JOIN {{source('poker','jugadores')}} j