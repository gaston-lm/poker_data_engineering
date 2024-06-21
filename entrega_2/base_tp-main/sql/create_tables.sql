CREATE TABLE IF NOT EXISTS Jugadores (
    id_jugador INTEGER PRIMARY KEY,
    nombre TEXT,
    apellido TEXT
);

CREATE TABLE IF NOT EXISTS Partidos (
    id_partido INTEGER PRIMARY KEY,
    num_jugadores INTEGER,
    hora_inicio TIMESTAMP,
    duracion INTEGER
);

CREATE TABLE IF NOT EXISTS Manos (
    mano_en_partido INTEGER,
    id_partido INTEGER REFERENCES Partidos(id_partido),
    PRIMARY KEY (mano_en_partido, id_partido)
);

CREATE TABLE IF NOT EXISTS Cartas (
    id_carta INTEGER PRIMARY KEY,
    palo VARCHAR(10),
    valor VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS JugadoresJueganCon (
    id_partido INTEGER,
    mano_en_partido INTEGER,
    id_jugador INTEGER REFERENCES Jugadores(id_jugador),
    id_carta_1 INTEGER REFERENCES Cartas(id_carta),
    id_carta_2 INTEGER REFERENCES Cartas(id_carta),
    orden INTEGER,
    es_ganador BOOLEAN, -- en la primera entrega pusimos integer: chequear como afecta el resto.
    PRIMARY KEY (id_partido, mano_en_partido, id_jugador),
    FOREIGN KEY (id_partido, mano_en_partido) REFERENCES Manos(id_partido, mano_en_partido),
    CONSTRAINT unique_cartas_jugador_en_mano UNIQUE (id_partido, mano_en_partido, id_carta_1, id_carta_2),
    CONSTRAINT unique_cartas_mismo_jugador CHECK (id_carta_1 <> id_carta_2)
);

CREATE TABLE IF NOT EXISTS Rondas (
    ronda_en_mano INTEGER,
    id_partido INTEGER,
    mano_en_partido INTEGER,
    PRIMARY KEY (ronda_en_mano, id_partido, mano_en_partido),
    FOREIGN KEY (id_partido, mano_en_partido) REFERENCES Manos(id_partido, mano_en_partido)
);

CREATE TABLE IF NOT EXISTS JugadoresEnRonda(
    ronda_en_mano INTEGER,
    id_partido INTEGER,
    mano_en_partido INTEGER,
    id_jugador INTEGER REFERENCES Jugadores(id_jugador),
    apuesta INTEGER,
    dinero_disponible INTEGER,
    PRIMARY KEY (ronda_en_mano, id_partido, mano_en_partido, id_jugador),
    FOREIGN KEY (ronda_en_mano, id_partido, mano_en_partido) REFERENCES Rondas(ronda_en_mano, id_partido, mano_en_partido),
    CONSTRAINT apuesta_menor_a_disponible CHECK (apuesta <= dinero_disponible)
);

CREATE TABLE IF NOT EXISTS CartasEnRonda (
    ronda_en_mano INTEGER,
    id_partido INTEGER,
    mano_en_partido INTEGER,
    id_carta INTEGER REFERENCES Cartas(id_carta),
    PRIMARY KEY (ronda_en_mano, id_partido, mano_en_partido, id_carta),
    FOREIGN KEY (ronda_en_mano, id_partido, mano_en_partido) REFERENCES Rondas(ronda_en_mano, id_partido, mano_en_partido),
    CONSTRAINT unique_cartas_en_mano UNIQUE (id_partido, mano_en_partido, id_carta)
);