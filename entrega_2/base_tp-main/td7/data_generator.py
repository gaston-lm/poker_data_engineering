import datetime
import random
from faker import Faker
from faker.providers import address, date_time, internet, passport, phone_number
import uuid

from td7.custom_types import Records, Record

CARTAS = [
    {"id_carta": 1, "palo": "diamonds", "valor": "A"},
    {"id_carta": 2, "palo": "hearts", "valor": "A"},
    {"id_carta": 3, "palo": "spades", "valor": "A"},
    {"id_carta": 4, "palo": "clubs", "valor": "A"},
    {"id_carta": 5, "palo": "diamonds", "valor": "K"},
    {"id_carta": 6, "palo": "hearts", "valor": "K"},
    {"id_carta": 7, "palo": "spades", "valor": "K"},
    {"id_carta": 8, "palo": "clubs", "valor": "K"},
    {"id_carta": 9, "palo": "diamonds", "valor": "Q"},
    {"id_carta": 10, "palo": "hearts", "valor": "Q"},
    {"id_carta": 11, "palo": "spades", "valor": "Q"},
    {"id_carta": 12, "palo": "clubs", "valor": "Q"},
    {"id_carta": 13, "palo": "diamonds", "valor": "J"},
    {"id_carta": 14, "palo": "hearts", "valor": "J"},
    {"id_carta": 15, "palo": "spades", "valor": "J"},
    {"id_carta": 16, "palo": "clubs", "valor": "J"},
    {"id_carta": 17, "palo": "diamonds", "valor": "9"},
    {"id_carta": 18, "palo": "hearts", "valor": "9"},
    {"id_carta": 19, "palo": "spades", "valor": "9"},
    {"id_carta": 20, "palo": "clubs", "valor": "9"},
    {"id_carta": 21, "palo": "diamonds", "valor": "8"},
    {"id_carta": 22, "palo": "hearts", "valor": "8"},
    {"id_carta": 23, "palo": "spades", "valor": "8"},
    {"id_carta": 24, "palo": "clubs", "valor": "8"},
    {"id_carta": 25, "palo": "diamonds", "valor": "7"},
    {"id_carta": 26, "palo": "hearts", "valor": "7"},
    {"id_carta": 27, "palo": "spades", "valor": "7"},
    {"id_carta": 28, "palo": "clubs", "valor": "7"},
    {"id_carta": 29, "palo": "diamonds", "valor": "6"},
    {"id_carta": 30, "palo": "hearts", "valor": "6"},
    {"id_carta": 31, "palo": "spades", "valor": "6"},
    {"id_carta": 32, "palo": "clubs", "valor": "6"},
    {"id_carta": 33, "palo": "diamonds", "valor": "5"},
    {"id_carta": 34, "palo": "hearts", "valor": "5"},
    {"id_carta": 35, "palo": "spades", "valor": "5"},
    {"id_carta": 36, "palo": "clubs", "valor": "5"},
    {"id_carta": 37, "palo": "diamonds", "valor": "4"},
    {"id_carta": 38, "palo": "hearts", "valor": "4"},
    {"id_carta": 39, "palo": "spades", "valor": "4"},
    {"id_carta": 40, "palo": "clubs", "valor": "4"},
    {"id_carta": 41, "palo": "diamonds", "valor": "3"},
    {"id_carta": 42, "palo": "hearts", "valor": "3"},
    {"id_carta": 43, "palo": "spades", "valor": "3"},
    {"id_carta": 44, "palo": "clubs", "valor": "3"},
    {"id_carta": 45, "palo": "diamonds", "valor": "2"},
    {"id_carta": 46, "palo": "hearts", "valor": "2"},
    {"id_carta": 47, "palo": "spades", "valor": "2"},
    {"id_carta": 48, "palo": "clubs", "valor": "2"}
]

JUGADORES = [
    {"id_jugador": 1, "nombre": "Gaston", "apellido": "Loza"},
    {"id_jugador": 2, "nombre": "Valentin", "apellido": "Bonas"},
    {"id_jugador": 3, "nombre": "Federico", "apellido": "Giorgi"},
    {"id_jugador": 4, "nombre": "Tomas", "apellido": "Curzio"},
    {"id_jugador": 5, "nombre": "Javier", "apellido": "Mermet"},
    {"id_jugador": 6, "nombre": "Ignacio", "apellido": "Perez"},
    {"id_jugador": 7, "nombre": "Pablo", "apellido": "Piccoli"},
    {"id_jugador": 8, "nombre": "Chantal", "apellido": "Levi"},
    {"id_jugador": 9, "nombre": "Pilar", "apellido": "Solari"},
    {"id_jugador": 10, "nombre": "Lara", "apellido": "Moglie"},
    {"id_jugador": 11, "nombre": "Elizabeth", "apellido": "Wurzel"},
    {"id_jugador": 12, "nombre": "Paula", "apellido": "Kuna"},
    {"id_jugador": 13, "nombre": "Cecilia", "apellido": "Bari"},
    {"id_jugador": 14, "nombre": "Emmanuel", "apellido": "Iarussi"},
    {"id_jugador": 15, "nombre": "Agustin", "apellido": "Gravano"},
    {"id_jugador": 16, "nombre": "Daniela", "apellido": "Cuesta"}
]


class DataGenerator:
    def __init__(self):
        """Instantiates faker instance"""
        self.fake = Faker()
        self.fake.add_provider(passport)
        # esto en realidad habría que hacer que se extraigan de la DB
        self.cards = CARTAS 
        self.jugadores = JUGADORES

    def generate_jugadores(self, n: int) -> Records:
        """Generates n jugadores (players).

        Parameters
        ----------
        n : int
            Number of players to generate.

        Returns
        -------
        list[dict[str, Any]]
            List of dicts that include id_jugador, nombre, apellido.
        """
        jugadores = []
        for i in range(n):
            jugadores.append(
                {
                    "id_jugador": self.fake.unique.passport_number(),
                    "nombre": self.fake.unique.first_name(),
                    "apellido": self.fake.unique.last_name()
                }
            )
        return jugadores

    def generate_partido(self, id: int):
        """Generates all things necessary to keep consistency withing a partido (game)

        Parameters
        ----------
        id : int
            Previous ID number of games.

        """
        partido: Record = {
                    "id_partido": id + 1,
                    "num_jugadores": random.randint(2, 8),
                    "hora_inicio": self.fake.date_time_this_year(),
                    "duracion": random.randint(30, 180)  # duration in minutes --> esto en la entrega 1 dijeron q estaba mal
                }
        print("Partido: ", partido)

        manos: Records = self.generate_manos(partido)
        print("manos: ", manos)

        jugadores: Records = random.sample(self.jugadores, partido["num_jugadores"])

        jug_con = self.generate_jugadores_juegan_con(manos, jugadores)
        jugadores_juegan_con: Records = jug_con[0]
        cartas_asignadas: list[set[int]] = jug_con[1]
        print("jugadores_juegan_con: ", jugadores_juegan_con)

        f_rondas = self.generate_rondas(manos)
        rondas : Records = f_rondas[0]
        num_rondas_por_mano: list[int] = f_rondas[1]
        print("rondas: ", rondas)

        cartas_en_ronda = self.generate_cartas_en_ronda(manos, cartas_asignadas, num_rondas_por_mano)
        print("cartas_en_ronda: ", cartas_en_ronda)

        jugadores_en_ronda = self.generate_jugadores_en_ronda(rondas, jugadores)
        print("jugadores_en_ronda: ", jugadores_en_ronda)


    def generate_manos(self, partido: Record) -> Records:
        """Generates manos (hands) for a particular partido (match).

        Parameters
        ----------
        partido : dict[str, any]
            Match record.

        Returns
        -------
        list[dict[str, Any]]
            List of dicts that include mano_en_partido, id_partido.
        """
        manos = []
        
        num_manos = random.randint(1, 5)
        for mano in range(num_manos):
            manos.append(
                {
                    "mano_en_partido": mano + 1,
                    "id_partido": partido["id_partido"]
                }
            )

        return manos

    def generate_jugadores_juegan_con(self, manos: Records, jugadores: Records) -> tuple[Records, list[set[int]]]:
        """Generates jugadores_juegan_con (players playing with cards) entries.

        Parameters
        ----------
        manos : list[dict[str, any]]
            List of hands.
        jugadores : list[dict[str, any]]
            List of players.

        Returns
        -------
        list[dict[str, Any]]
            List of dicts that include id_partido, mano_en_partido, id_jugador, id_carta_1, id_carta_2, orden, es_ganador.
        list[det[int]]
            List of set of cards assign to each hand (to avoid repetition in table cards)
        """
        jugadores_juegan_con = []
        used_cards_by_hand = []
        for mano in manos:
            used_cards = set()
            winner = random.sample(jugadores, 1)[0]

            for orden, jugador in enumerate(jugadores, start=1):
                cartas_en_juego = random.sample(self.cards, 2)
                
                # Ensure that the selected cards are not already used in this hand
                while (cartas_en_juego[0]["id_carta"] in used_cards or cartas_en_juego[1]["id_carta"] in used_cards):
                    cartas_en_juego = random.sample(self.cards, 2)

                # Add the selected cards to the set of used cards
                used_cards.add(cartas_en_juego[0]["id_carta"])
                used_cards.add(cartas_en_juego[1]["id_carta"])

                condition = False
                if jugador == winner:
                    condition = True

                jugadores_juegan_con.append(
                    {
                        "id_partido": mano["id_partido"],
                        "mano_en_partido": mano["mano_en_partido"],
                        "id_jugador": jugador["id_jugador"],
                        "id_carta_1": cartas_en_juego[0]["id_carta"],
                        "id_carta_2": cartas_en_juego[1]["id_carta"],
                        "orden": orden,
                        "es_ganador": condition
                    }
                )
            
            used_cards_by_hand.append(used_cards)

        return jugadores_juegan_con, used_cards_by_hand

    def generate_rondas(self, manos: Records) -> tuple[Records, list[int]]:
        """Generates rondas (rounds) for each mano (hand).

        Parameters
        ----------
        manos : list[dict[str, any]]
            List of hands.

        Returns
        -------
        list[dict[str, Any]]
            List of dicts that include ronda_en_mano, id_partido, mano_en_partido.
        list[int]
            List of number of rounds per hand
        """
        rondas = []
        num_rondas_por_mano = []
        for mano in manos:
            num_rondas = random.randint(1, 10)
            num_rondas_por_mano.append(num_rondas)
            for ronda in range(num_rondas):
                rondas.append(
                    {
                        "ronda_en_mano": ronda + 1,
                        "id_partido": mano["id_partido"],
                        "mano_en_partido": mano["mano_en_partido"]
                    }
                )

        return rondas, num_rondas_por_mano

    def generate_cartas_en_ronda(self, manos: Records, cartas_usadas: list[set[int]], num_rondas_por_mano: list[int]) -> Records:
        """Generates cartas_en_ronda (cards in round) entries.

        Parameters
        ----------
        rondas : list[dict[str, any]]
            List of rounds.
        cartas_usadas : list[set[int]]
            List of sets of cards used in each hand.
        num_rondas_por_mano : list[int]
            List of number of rounds per hand

        Returns
        -------
        List[Dict[str, Any]]
            List of dicts that include ronda_en_mano, id_partido, mano_en_partido, id_carta.
        """
        cartas_en_ronda = []

        for i, mano in enumerate(manos):
            if num_rondas_por_mano[i] >= 2:
                # Generar las primeras 3 cartas del croupier
                for _ in range(3):
                    carta = random.sample(self.cards, 1)[0]

                    # Ensure that the selected cards are not already used in this hand
                    while carta["id_carta"] in cartas_usadas[i]:
                        carta = random.sample(self.cards, 1)[0]

                    cartas_en_ronda.append(
                        {
                            "ronda_en_mano": 2,
                            "id_partido": mano["id_partido"],
                            "mano_en_partido": mano["mano_en_partido"],
                            "id_carta": carta
                        }
                    )
                    cartas_usadas[i].add(carta["id_carta"])

            if num_rondas_por_mano[i] >= 3:
                carta = random.sample(self.cards, 1)[0]
                
                # Ensure that the selected cards are not already used in this hand
                while carta["id_carta"] in cartas_usadas[i]:
                    carta = random.sample(self.cards, 1)[0]

                cartas_en_ronda.append(
                    {
                        "ronda_en_mano": 3,
                        "id_partido": mano["id_partido"],
                        "mano_en_partido": mano["mano_en_partido"],
                        "id_carta": carta
                    }
                )
                cartas_usadas[i].add(carta["id_carta"])

            if num_rondas_por_mano[i] >= 4:
                carta = random.sample(self.cards, 1)[0]
                
                # Ensure that the selected cards are not already used in this hand
                while carta["id_carta"] in cartas_usadas[i]:
                    carta = random.sample(self.cards, 1)[0]

                cartas_en_ronda.append(
                    {
                        "ronda_en_mano": 4,
                        "id_partido": mano["id_partido"],
                        "mano_en_partido": mano["mano_en_partido"],
                        "id_carta": carta
                    }
                )
                cartas_usadas[i].add(carta["id_carta"])

        return cartas_en_ronda

    def generate_jugadores_en_ronda(self, rondas: Records, jugadores: Records) -> Records:
        """Generates jugadores_en_ronda (players in round) entries.

        Parameters
        ----------
        rondas : List[Dict[str, any]]
            List of rounds.
        jugadores : List[Dict[str, any]]
            List of players.

        Returns
        -------
        List[Dict[str, Any]]
            List of dicts that include ronda_en_mano, id_partido, mano_en_partido, id_jugador, apuesta, dinero_disponible.
        """
        # IDEA:
        # - vector con plata disponible para cada uno de los jugadores (tuplas jugador, dinero_disponible tal vez)
        # - que la apuesta sea entre 0 y dinero_disponible (si es 0 hay que sacarlo de la lista de jugadores para la proxima)

        jugadores_activos: list[list[Record | int]] = [] 
        for jugador in jugadores:
            dinero_disponible = random.randint(100, 100000)
            jugadores_activos.append([jugador, dinero_disponible])

        jugadores_en_ronda = []

        for ronda in rondas:
            for tup_jugador in jugadores_activos:
                jugador = tup_jugador[0]
                dinero_disponible = tup_jugador[1]
                se_va = random.choice([True, True, False, False, False, False, False, False, False, False])
                apuesta = 0

                if not se_va:
                    apuesta = random.randint(0, dinero_disponible)

                jugadores_en_ronda.append(
                    {
                        "ronda_en_mano": ronda["ronda_en_mano"],
                        "id_partido": ronda["id_partido"],
                        "mano_en_partido": ronda["mano_en_partido"],
                        "id_jugador": jugador["id_jugador"],
                        "apuesta": apuesta,
                        "dinero_disponible": dinero_disponible
                    }
                )
                if se_va or apuesta == 0:
                    jugadores_activos.remove(tup_jugador)
                else:
                    tup_jugador[1] -= apuesta

        return jugadores_en_ronda

# Example usage
if __name__ == "__main__":
    generator = DataGenerator()

    # Generate players
    # jugadores = generator.generate_jugadores(5)
    # print("Jugadores:", jugadores)

    generator.generate_partido(0)
