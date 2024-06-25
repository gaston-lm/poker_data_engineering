from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
import pendulum
import datetime
from td7.data_generator import DataGenerator
from td7.schema import Schema

EVENTS_PER_DAY = 10

def _total_bets_last_week():
    schema = Schema()
    total_bet = int(schema.get_last_week_total_bet()[0]['total_apuesta'])

    if total_bet > 15000000:
        return 'internal_external_report'
    else:
        return 'internal_report'

def _generate_data(base_time: str, n: int):
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

    jugadores = generator.generate_jugadores(10)
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
        num_partidos += 1 # --> preguntar esto

with DAG(
    "fill_data",
    start_date=pendulum.datetime(2024, 6, 1, tz="UTC"),
    schedule_interval="@monthly",
    catchup=True,
) as dag:
    op = PythonOperator(
        task_id="genrate_games",
        python_callable=_generate_data,
        op_kwargs=dict(n=EVENTS_PER_DAY, base_time="{{ ds }}"),
    )

    op2 = BranchPythonOperator(
        task_id="get_bets",
        python_callable=_total_bets_last_week,
        op_kwargs=dict(base_time="{{ ds }}"),
    )

    op3_a = DummyOperator(task_id='internal_external_report')
    op3_b = DummyOperator(task_id='internal_report')

    op >> op2 >> [op3_a, op3_b]