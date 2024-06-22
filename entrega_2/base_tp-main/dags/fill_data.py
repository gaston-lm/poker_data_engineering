from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
import pendulum
import datetime
from td7.data_generator import DataGenerator
from td7.schema import Schema

EVENTS_PER_DAY = 10

def generate_once():
    generator = DataGenerator()
    schema = Schema()
    # Por única vez cargo en sistema las 48 cartas
    cards = generator.generate_cards()
    schema.insert(cards, "cartas")
    # Por única vez cargo en sistema los primeros 30 jugadores
    jugadores = generator.generate_jugadores(30)
    schema.insert(jugadores, "jugadores")

def generate_data(base_time: str, n: int):
    """Generates synth data and saves to DB.

    Parameters
    ----------
    base_time: strpoetry export --without-hashes --format=requirements.txt > requirements.txt

        Base datetime to start events from.
    n : int
        Number of events to generate.
    """
    generator = DataGenerator()
    schema = Schema()

    jugadores = generator.generate_jugadores(5)
    schema.insert(jugadores, "jugadores")

    num_partidos = int(schema.get_games_num()[0]['count'])
    frequency = datetime.timedelta(days=1) / n
    base_time = datetime.datetime.fromisoformat(base_time)

    for i in range(n):
        sample_jugadores = schema.get_players()
        cards = schema.get_cards()
        date_time =  base_time + i * frequency
        partido, manos, jugadores_juegan_con, rondas, cartas_en_ronda, jugadores_en_ronda = generator.generate_partido(num_partidos, sample_jugadores, cards, date_time)

        schema.insert(partido, "partidos")
        schema.insert(manos, "manos")
        schema.insert(jugadores_juegan_con, "jugadoresjuegancon")
        schema.insert(rondas, "rondas")
        schema.insert(cartas_en_ronda, "cartasenronda")
        schema.insert(jugadores_en_ronda, "jugadoresenronda")
        num_partidos += 1

with DAG(
    "fill_cards",
    start_date=pendulum.datetime(2024, 6, 1, tz="UTC"),
    schedule_interval="@once",
    catchup=True,
) as dag:
    op = PythonOperator(
        task_id="cards_players_generator",
        python_callable=generate_once,
    )

with DAG(
    "fill_data",
    start_date=pendulum.datetime(2024, 6, 1, tz="UTC"),
    schedule_interval="@monthly",
    catchup=True,
) as dag:
    op = PythonOperator(
        task_id="genrate_games",
        python_callable=generate_data,
        op_kwargs=dict(n=EVENTS_PER_DAY, base_time="{{ ds }}"),
    )
