-- 1) Encontrar el partido que más manos tuvo

SELECT id_partido, count(*)
FROM manos
GROUP BY id_partido
ORDER BY count(*) DESC
LIMIT 1;

-- 2) Encontrar para cada jugador, cuantas manos ganó mostrando su nombre y apellido. Debe 
--    estar ordenado según la cantidad de manera descendente.

SELECT 
	j.nombre, 
	j.apellido, 
	count(*)
FROM 
	jugadoresjuegancon jjc
NATURAL JOIN 
	jugadores j
GROUP BY 
	j.id_jugador , j.nombre, j.apellido, jjc.es_ganador
HAVING 
	jjc.es_ganador = 1
ORDER BY
	count(*) DESC;

-- 3) Encontrar quién fue el jugador que ganó más plata en todos sus partidos

WITH total_apostado_por_mano AS (
	SELECT jr.id_partido, jr.mano_en_partido, sum(jr.apuesta) AS total_apostado
	FROM jugadoresenronda jr
	GROUP BY jr.id_partido, jr.mano_en_partido
)

SELECT
	j.nombre, j.apellido, sum(t.total_apostado)
FROM
	jugadoresjuegancon jjc
NATURAL JOIN
	jugadores j
INNER JOIN
	total_apostado_por_mano t ON t.id_partido = jjc.id_partido AND t.mano_en_partido = jjc.mano_en_partido 
GROUP BY 
	j.id_jugador, j.nombre, j.apellido, jjc.es_ganador
HAVING 
	jjc.es_ganador = 1
ORDER BY 
	sum(t.total_apostado) DESC
LIMIT 1; 

	
-- 4) Dado un partido, ver el ranking de jugadores que tiene el perfil más conservador, es decir 
--    que jugó menos rondas.
	
SELECT 
	j.nombre, 
	j.apellido,
	count(*)
FROM 
	jugadoresenronda jr
INNER JOIN
	jugadores j ON j.id_jugador = jr.id_jugador 
WHERE 
	jr.id_partido = 2
GROUP BY 
	jr.id_jugador, j.nombre, j.apellido
ORDER BY 
	count(*) ASC;

-- 5) Para cada ronda de un partido en específico calcular la diferencia de lo apostado por cada jugador 
--    con respecto a la ronda anterior y indicar si "se achico" o se "se agrando".

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
	FROM jugadoresenronda jr
)

SELECT 
	dj.mano_en_partido, 
	dj.ronda_en_mano,
	j.nombre AS nombre_jugador,
	j.apellido AS apellido_jugador,
	dj.apuesta,
	CASE 
		WHEN dj.diferencia_apuesta <= 0 THEN 'se achicó'
		WHEN dj.diferencia_apuesta > 0 THEN 'se agrandó'
		ELSE 'primera apuesta'
	END
FROM diferencias_jugadores dj
NATURAL JOIN jugadores j
WHERE dj.id_partido = '1';

-- 6) Encontrar todas veces que los jugadores tuvieron poker, indicando el partido, mano, nombre y apellido.

WITH 
	cartas_por_mano AS (
		SELECT 
			c.id_partido,
			c.mano_en_partido,
			c.id_carta AS id_primera_carta, 
			lag(c.id_carta, 1) OVER (PARTITION BY c.id_partido, c.mano_en_partido ORDER BY c.id_carta) AS id_segunda_carta,
			lag(c.id_carta, 2) OVER (PARTITION BY c.id_partido, c.mano_en_partido ORDER BY c.id_carta) AS id_tercera_carta,
			lag(c.id_carta, 3) OVER (PARTITION BY c.id_partido, c.mano_en_partido ORDER BY c.id_carta) AS id_cuarta_carta,
			lag(c.id_carta, 4) OVER (PARTITION BY c.id_partido, c.mano_en_partido ORDER BY c.id_carta) AS id_quinta_carta,
			max(c.id_carta) OVER (PARTITION BY c.id_partido, c.mano_en_partido) AS fila_interes
		FROM cartasenronda c
	),
	juego_de_cartas_por_jugador AS (
		SELECT
			cm.id_partido,
			cm.mano_en_partido,
			jjc.id_jugador,
			cm.id_primera_carta, 
			cm.id_segunda_carta, 
			cm.id_tercera_carta, 
			cm.id_cuarta_carta, 
			cm.id_quinta_carta, 
			jjc.id_carta_1, 
			jjc.id_carta_2 
		FROM 
			cartas_por_mano cm
		JOIN 
			jugadoresjuegancon jjc ON 
				jjc.id_partido = cm.id_partido AND jjc.mano_en_partido = cm.mano_en_partido
		WHERE 
			id_primera_carta = fila_interes
	),
	valores_cartas_por_juego AS (
		SELECT
			jc.id_partido,
			jc.mano_en_partido,
			jc.id_jugador,
			c1.valor AS v1, 
			c2.valor AS v2, 
			c3.valor AS v3, 
			c4.valor AS v4, 
			c5.valor AS v5, 
			c6.valor AS v6, 
			c7.valor AS v7
		FROM juego_de_cartas_por_jugador jc
		INNER JOIN cartas c1 ON c1.id_carta = jc.id_primera_carta
		INNER JOIN cartas c2 ON c2.id_carta = jc.id_segunda_carta
		INNER JOIN cartas c3 ON c3.id_carta = jc.id_tercera_carta
		INNER JOIN cartas c4 ON c4.id_carta = jc.id_cuarta_carta
		INNER JOIN cartas c5 ON c5.id_carta = jc.id_quinta_carta
		INNER JOIN cartas c6 ON c6.id_carta = jc.id_carta_1
		INNER JOIN cartas c7 ON c7.id_carta = jc.id_carta_2
	),
	con_poker AS (
		SELECT 
			id_partido,
			mano_en_partido,
			id_jugador,
			CASE -- sabemos que esto NO es lo mejor, NO se nos ocurrió otra alternitva :(
				WHEN v6 = v5 AND v6 = v4 AND v6 = v3 THEN 'yes'
				WHEN v6 = v5 AND v6 = v4 AND v6 = v2 THEN 'yes'
				WHEN v6 = v5 AND v6 = v4 AND v6 = v1 THEN 'yes'
				WHEN v6 = v5 AND v6 = v2 AND v6 = v3 THEN 'yes'
				WHEN v6 = v5 AND v6 = v2 AND v6 = v1 THEN 'yes'
				WHEN v6 = v5 AND v6 = v3 AND v6 = v1 THEN 'yes'
				WHEN v6 = v2 AND v6 = v4 AND v6 = v3 THEN 'yes'
				WHEN v6 = v1 AND v6 = v4 AND v6 = v2 THEN 'yes'
				WHEN v6 = v3 AND v6 = v4 AND v6 = v1 THEN 'yes'
				WHEN v6 = v1 AND v6 = v2 AND v6 = v3 THEN 'yes'
				
				WHEN v7 = v5 AND v7 = v4 AND v7 = v3 THEN 'yes'
				WHEN v7 = v5 AND v7 = v4 AND v7 = v2 THEN 'yes'
				WHEN v7 = v5 AND v7 = v4 AND v7 = v1 THEN 'yes'
				WHEN v7 = v5 AND v7 = v2 AND v7 = v3 THEN 'yes'
				WHEN v7 = v5 AND v7 = v2 AND v7 = v1 THEN 'yes'
				WHEN v7 = v5 AND v7 = v3 AND v7 = v1 THEN 'yes'
				WHEN v7 = v2 AND v7 = v4 AND v7 = v3 THEN 'yes'
				WHEN v7 = v1 AND v7 = v4 AND v7 = v2 THEN 'yes'
				WHEN v7 = v3 AND v7 = v4 AND v7 = v1 THEN 'yes'
				WHEN v7 = v1 AND v7 = v2 AND v7 = v3 THEN 'yes'
				
				WHEN v7 = v6 AND v7 = v4 AND v7 = v3 THEN 'yes'
				WHEN v7 = v6 AND v7 = v4 AND v7 = v2 THEN 'yes'
				WHEN v7 = v6 AND v7 = v4 AND v7 = v1 THEN 'yes'
				WHEN v7 = v6 AND v7 = v2 AND v7 = v3 THEN 'yes'
				WHEN v7 = v6 AND v7 = v2 AND v7 = v1 THEN 'yes'
				WHEN v7 = v6 AND v7 = v3 AND v7 = v1 THEN 'yes'
				WHEN v7 = v6 AND v7 = v5 AND v7 = v3 THEN 'yes'
				WHEN v7 = v6 AND v7 = v5 AND v7 = v2 THEN 'yes'
				WHEN v7 = v6 AND v7 = v5 AND v7 = v1 THEN 'yes'
				WHEN v7 = v6 AND v7 = v5 AND v7 = v4 THEN 'yes'
				ELSE 'no'	
			END AS es_poker
		FROM 
			valores_cartas_por_juego vc
	)

SELECT 
	cp.id_partido,
	cp.mano_en_partido,
	j.nombre,
	j.apellido
FROM 
	con_poker cp
INNER JOIN 
	jugadores j ON cp.id_jugador = j.id_jugador 
WHERE
	cp.es_poker = 'yes';


-- 7) Para cada partido contar la cantidad de manos en las que el croupier no llegó a develar las 5 cartas.
	
WITH 
	cartas_por_mano AS (
		SELECT 
			c.id_partido,
			c.mano_en_partido,
			c.id_carta AS id_primera_carta, 
			lag(c.id_carta, 1) OVER (PARTITION BY c.id_partido, c.mano_en_partido ORDER BY c.id_carta) AS id_segunda_carta,
			lag(c.id_carta, 2) OVER (PARTITION BY c.id_partido, c.mano_en_partido ORDER BY c.id_carta) AS id_tercera_carta,
			lag(c.id_carta, 3) OVER (PARTITION BY c.id_partido, c.mano_en_partido ORDER BY c.id_carta) AS id_cuarta_carta,
			lag(c.id_carta, 4) OVER (PARTITION BY c.id_partido, c.mano_en_partido ORDER BY c.id_carta) AS id_quinta_carta,
			max(c.id_carta) OVER (PARTITION BY c.id_partido, c.mano_en_partido) AS fila_interes
		FROM cartasenronda c
	),
	sin_mostrar_todas AS (
	SELECT
		cm.id_partido, cm.mano_en_partido, cm.id_primera_carta, cm.id_segunda_carta, cm.id_tercera_carta, cm.id_cuarta_carta, cm.id_quinta_carta
	FROM
		cartas_por_mano cm
	WHERE 
		cm.id_primera_carta = cm.fila_interes AND (
		cm.id_tercera_carta IS NULL OR 
		cm.id_cuarta_carta IS NULL OR 
		cm.id_quinta_carta IS NULL)
	)

SELECT id_partido, count(*) AS cantidad_manos
FROM sin_mostrar_todas
GROUP BY id_partido;

-- 8) Devolver todos los jugadores que alguna vez hicieron un all-in (apostaron todo).

SELECT DISTINCT 
	j.nombre, j.apellido, jr.id_partido, jr.mano_en_partido
FROM 
	jugadoresenronda jr 
INNER JOIN 
	jugadores j ON j.id_jugador = jr.id_jugador 
WHERE 
	jr.apuesta = jr.dinero_disponible AND jr.dinero_disponible != 0;

-- 9) Encontrar los jugadores que tuvieron un par con sus dos cartas propias, en qué mano le ocurrió y con qué valor.

SELECT
	 j.nombre, j.apellido, jjc.id_partido, jjc.mano_en_partido, c1.valor
FROM
	jugadoresjuegancon jjc
INNER JOIN
	jugadores j ON j.id_jugador = jjc.id_jugador
INNER JOIN 
	cartas c1 ON c1.id_carta = jjc.id_carta_1
INNER JOIN 
	cartas c2 ON c2.id_carta = jjc.id_carta_2
WHERE
	c1.valor = c2.valor;

-- 10) Cantidad de partidos jugados por cada jugador. Incluir aquellos que nunca jugaron.

WITH cantidad_jugaron AS (
	SELECT
		id_jugador, count(*) AS cantidad_partidos
	FROM (
		SELECT DISTINCT 
			id_jugador, id_partido 
		FROM
			jugadoresjuegancon
		)
	GROUP BY 
		id_jugador
)

SELECT 
	j.id_jugador, 
	j.nombre, 
	j.apellido, 
	COALESCE(c.cantidad_partidos, 0) AS cantidad_partidos
FROM 
	cantidad_jugaron c
RIGHT OUTER JOIN 
	jugadores j ON j.id_jugador = c.id_jugador

