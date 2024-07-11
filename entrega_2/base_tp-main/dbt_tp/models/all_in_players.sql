{{ config(materialized='table') }}

SELECT DISTINCT 
	j.id_jugador, j.nombre, j.apellido, jr.id_partido, jr.mano_en_partido
FROM 
	{{source('poker','jugadoresenronda')}} jr 
INNER JOIN 
	{{source('poker','jugadores')}} j ON j.id_jugador = jr.id_jugador 
INNER JOIN
	{{source('poker', 'partidos')}} p ON p.id_partido = jr.id_partido
WHERE 
	jr.apuesta = jr.dinero_disponible AND jr.dinero_disponible != 0 AND p.hora_inicio >= NOW() - INTERVAL '7 days'
