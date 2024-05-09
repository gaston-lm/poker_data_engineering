CREATE TABLE Jugadores (
    id_jugador INTEGER PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50)
);

CREATE TABLE Partidos (
    id_partido INTEGER PRIMARY KEY,
    num_jugadores INTEGER,
    hora_inicio TIMESTAMP,
    duracion INTEGER
);

CREATE TABLE Manos (
    mano_en_partido INTEGER,
    id_partido INTEGER REFERENCES Partidos(id_partido),
    jugador_ganador INTEGER REFERENCES Jugadores(id_jugador),
    PRIMARY KEY (mano_en_partido, id_partido)
);

CREATE TABLE Cartas (
    id_cartas INTEGER PRIMARY KEY,
    palo VARCHAR(10),
    valor VARCHAR(10)
);

CREATE TABLE JugadorTieneEn (
    id_partido INTEGER,
    mano_en_partido INTEGER,
    id_jugador INTEGER REFERENCES Jugadores(id_jugador),
    id_carta_1 INTEGER REFERENCES Cartas(id_cartas),
    id_carta_2 INTEGER REFERENCES Cartas(id_cartas),
    PRIMARY KEY (id_partido, mano_en_partido, id_jugador),
    FOREIGN KEY (id_partido, mano_en_partido) REFERENCES Manos(id_partido, mano_en_partido)
);

CREATE TABLE Rondas (
    ronda_en_mano INTEGER,
    id_partido INTEGER,
    mano_en_partido INTEGER,
    PRIMARY KEY (ronda_en_mano, id_partido, mano_en_partido),
    FOREIGN KEY (id_partido, mano_en_partido) REFERENCES Manos(id_partido, mano_en_partido)
);

CREATE TABLE JugadoresEnRonda(
    ronda_en_mano INTEGER,
    id_partido INTEGER,
    mano_en_partido INTEGER,
    id_jugador INTEGER REFERENCES Jugadores(id_jugador),
    apuesta INTEGER,
    dinero_disponible INTEGER,
    PRIMARY KEY (ronda_en_mano, id_partido, mano_en_partido, id_jugador),
    FOREIGN KEY (ronda_en_mano, id_partido, mano_en_partido) REFERENCES Rondas(ronda_en_mano, id_partido, mano_en_partido)
);

CREATE TABLE CartasEnRonda (
    ronda_en_mano INTEGER,
    id_partido INTEGER,
    mano_en_partido INTEGER,
    id_carta INTEGER REFERENCES Cartas(id_cartas),
    PRIMARY KEY (ronda_en_mano, id_partido, mano_en_partido, id_carta),
    FOREIGN KEY (ronda_en_mano, id_partido, mano_en_partido) REFERENCES Rondas(ronda_en_mano, id_partido, mano_en_partido)
);

CREATE TABLE OrdenEnMano (
    id_partido INTEGER,
    mano_en_partido INTEGER,
    id_jugador INTEGER REFERENCES Jugadores(id_jugador),
    orden INTEGER,
    PRIMARY KEY (id_partido, id_jugador),
    FOREIGN KEY (id_partido, mano_en_partido) REFERENCES Manos(id_partido, mano_en_partido)
);

--COPY your_table (first_name, last_name, age) FROM '' DELIMITER ';' CSV;

SELECT *
FROM partidos p 
WHERE duracion > 100 AND num_jugadores > 7