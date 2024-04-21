#### Dominio

Elegimos como dominio un conjunto de partidas de poker. Las partidas tendrán la información de en qué mesa se jugó, con cuantos jugadores, a qué hora comienzó y cuanto duró.

Dentro de cada juego, se registrará cada mano con las 5 cartas del croupier y las 2 cartas que le tocaron a cada jugador. Dentro de cada mano, se registrarán para cada ronda el orden en el que juegaron los jugadores y las decisiones que tomaron (retirarse, igualar la apuesta o apostar más). Además, se resgistrará el vencedor de la mano y su ganancia impactará en su saldo disponible. A su vez, los perdedores verán afectado su saldo también dado las apuestas que hayan hecho en las manos previas.

Por otro lado, para los jugadores se registrará su nombre, apellido y la cantidad de manos en las cuales resultó victorioso.

#### Relaciones

- Player(<u>player_id</u>, first_name, last_game, won_hands)

- Games(<u>game_id</u>, table_id, num_participants, begin_at, duration)

- Cards(<u>card_id</u>, suit, value)

- CardInHand(<u><span style='border-bottom: 1px dashed;'>game_id</span>, hand_in_game, <span style='border-bottom: 1px dashed;'>card_id</span></u>, owner, owner_id)
  - owner es croupier o player
  - owner_id es croupier_id o player_id

- Round(<u>round_in_hand, <span style='border-bottom: 1px dashed;'>game_id, hand_in_game, player_id</span></u>, bet, money_available) -> Restricción: el jugador siempre está asociado al mismo orden

- OrderInHand(<u><span style='border-bottom: 1px dashed;'>game_id, hand_in_game, player_id</span></u>, order)
  
- Hand(<u>hand_in_game, <span style='border-bottom: 1px dashed;'>game_id</span></u>, total_bet, winner_id) -> restricción: total_bet es la suma de todas las bet de rounds


