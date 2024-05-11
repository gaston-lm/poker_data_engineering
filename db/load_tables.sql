COPY cartas 
FROM '/docker-entrypoint-initdb.d/Cartas.csv'
DELIMITER ',' 
CSV HEADER
ENCODING 'LATIN1';

COPY jugadores 
FROM '/docker-entrypoint-initdb.d/Jugadores.csv'
DELIMITER ',' 
CSV HEADER
ENCODING 'LATIN1';

COPY partidos 
FROM '/docker-entrypoint-initdb.d/Partidos.csv'
DELIMITER ',' 
CSV HEADER
ENCODING 'LATIN1';

COPY manos 
FROM '/docker-entrypoint-initdb.d/Manos.csv'
DELIMITER ',' 
CSV HEADER
ENCODING 'LATIN1';

COPY rondas 
FROM '/docker-entrypoint-initdb.d/Rondas.csv'
DELIMITER ',' 
CSV HEADER
ENCODING 'LATIN1';

COPY jugadoresjuegancon
FROM '/docker-entrypoint-initdb.d/JugadoresJueganCon.csv'
DELIMITER ',' 
CSV HEADER
ENCODING 'LATIN1';

COPY jugadoresenronda 
FROM '/docker-entrypoint-initdb.d/JugadoresEnRonda.csv'
DELIMITER ',' 
CSV HEADER
ENCODING 'LATIN1';

COPY cartasenronda 
FROM '/docker-entrypoint-initdb.d/CartasEnRonda.csv'
DELIMITER ',' 
CSV HEADER
ENCODING 'LATIN1';