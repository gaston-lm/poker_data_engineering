{{ config(materialized='table') }}

SELECT DISTINCT 
	j.nombre, j.apellido, jr.id_partido, jr.mano_en_partido
FROM 
	{{source('poker','jugadoresenronda')}} jr 
INNER JOIN 
	{{source('poker','jugadores')}} j ON j.id_jugador = jr.id_jugador 
WHERE 
	jr.apuesta = jr.dinero_disponible AND jr.dinero_disponible != 0
