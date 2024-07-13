from typing import Optional

from td7.custom_types import Records
from td7.database import Database

class Schema:
    def __init__(self):
        self.db = Database()        
    
    def get_players(self) -> Records:
        return self.db.run_select("SELECT * FROM Jugadores" )

    def get_games(self) -> Records:
        return self.db.run_select("SELECT * FROM Partidos")

    def get_games_num(self):
        return self.db.run_select("SELECT COUNT(*) FROM Partidos")

    def get_last_week_total_bet(self,base_date):
        query = f"""
                WITH LastWeekPartidos AS (
                    SELECT id_partido
                    FROM Partidos
                    WHERE hora_inicio >= '{base_date}'::date - INTERVAL '7 days'
                )
                SELECT SUM(je.apuesta) AS total_apuesta
                FROM JugadoresEnRonda je
                JOIN Rondas r ON je.ronda_en_mano = r.ronda_en_mano 
                            AND je.id_partido = r.id_partido 
                            AND je.mano_en_partido = r.mano_en_partido
                JOIN LastWeekPartidos p ON je.id_partido = p.id_partido;
                """
                
        suma = self.db.run_select(query)
        print(suma)
        return suma
        
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
