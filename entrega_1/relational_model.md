## TP: Tecnología Digital VII

### Autores: Gaston Loza Montata & Valentín Bonás

#### Dominio

Elegimos como dominio un conjunto de partidos de poker. Los partidos tendrán la información cuantos jugadores participaron, a qué hora comenzó y cuanto duró.

Dentro de cada juego, se registrará cada mano con las 5 cartas del croupier y las 2 cartas que le tocaron a cada jugador. Dentro de cada mano, se registrarán para cada ronda el orden en el que juegaron los jugadores y las decisiones que tomaron (retirarse, igualar la apuesta o apostar más). 

Además, se resgistrará el vencedor de la mano y su ganancia impactará en su saldo disponible para la siguiente mano. A su vez, los perdedores verán afectado su saldo también dado las apuestas que hayan hecho en las manos previas. Dado que cada jugador comienza un partido con un monto de dinero independiente a sus otros partidos, nos enfocaremos en cómo su dinero se ve afectado desde el inicio del partido al final, pero no entre partidos. 

Por otro lado, para los jugadores se registrará su nombre, apellido y podremos calcular la cantidad de manos en las cuales resultó victorioso.

#### Modelo conceptual

Modelo entidad relación en el archivo `entity_relationship_model.pdf`.

#### Modelo lógico:

Modelo de tablas relacional:

- Jugadores(<u>id_jugador</u>, nombre, apellido)

- Partidos(<u>id_partido</u>, num_jugadores, hora_inicio, duracion)

- Manos(<u>mano_en_partido, <span style='border-bottom: 1px dashed;'>id_partido</span></u>)

- Cartas(<u>id_cartas</u>, palo, valor)

- JugadoresJuegaCon(<u><span style='border-bottom: 1px dashed;'>id_partido, mano_en_partido, id_jugador</u>, <span style='border-bottom: 1px dashed;'>id_carta_1, id_carta_2</span>, orden, es_ganador)

- Rondas(<u>ronda_en_mano, <span style='border-bottom: 1px dashed;'>id_partido, mano_en_partido</span></u>)

- JugadoresEnRondas(<span style='border-bottom: 1px dashed;'><u>ronda_en_mano, id_partido, mano_en_partido, id_jugador</span></u>, apuesta, dinero_disponible)

- CartasEnRonda(<span style='border-bottom: 1px dashed;'><u>ronda_en_mano, id_partido, mano_en_partido, id_carta</span></u>)