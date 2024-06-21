from typing import Optional

from td7.custom_types import Records
from td7.database import Database

class Schema:
    def __init__(self):
        self.db = Database()        
    
    def get_players(self, sample_n: Optional[int] = None) -> Records:
        query = "SELECT * FROM Jugadores"
        # preguntar esto para que?
        if sample_n is not None:
            query += f" LIMIT {sample_n}"
        
        return self.db.run_select(query)

    def get_games(self) -> Records:
        return self.db.run_select("SELECT * FROM Partidos")
    
    def get_hands(self) -> Records:
        return self.db.run_select("SELECT * FROM Manos")

    def get_cards(self) -> Records:
        return self.db.run_select("SELECT * FROM Cartas")

    def get_players_play_with(self) -> Records:
        return self.db.run_select("SELECT * FROM JugadoresJueganCon")
    
    def get_rounds(self) -> Records:
        return self.db.run_select("SELECT * FROM Rondas")

    def get_players_in_round(self) -> Records:
        return self.db.run_select("SELECT * FROM JugadoresEnRonda")

    def get_cards_in_round(self) -> Records:
        return self.db.run_select("SELECT * FROM CartasEnRonda")

    def insert(self, records: Records, table: str):
        self.db.run_insert(records, table)