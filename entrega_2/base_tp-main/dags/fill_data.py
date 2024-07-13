from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.dummy import DummyOperator
import pendulum
import datetime
from td7.data_generator import DataGenerator
from td7.schema import Schema
from airflow.utils.trigger_rule import TriggerRule


EVENTS_PER_DAY = 10

def _is_monday(base_time: str):
    execution_date = datetime.datetime.fromisoformat(base_time)
    if execution_date.weekday() == 0:  
        return 'wait_for_financial_data_completion'
    else:
        return 'skip_wait'

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
    start_date=pendulum.datetime(2024, 6, 25, tz="UTC"),
    schedule_interval="@daily",
    catchup=True,
) as dag:
    
    check_day = BranchPythonOperator(
        task_id='check_if_monday',
        python_callable=_is_monday,
        op_kwargs=dict(base_time="{{ ds }}"),
        provide_context=True,
    )

    wait_for_financial_data_completion = ExternalTaskSensor(
        task_id="wait_for_financial_data_completion",
        external_dag_id="financial_data",
        external_task_id="get_bets_branch", 
        mode="reschedule",
        timeout=8000,
        poke_interval=60,
        execution_date_fn=lambda exec_date: exec_date - datetime.timedelta(days=1)
    )

    skip_wait = DummyOperator(
        task_id='skip_wait',
    )

    generate_data = PythonOperator(
        task_id="generate_data",
        python_callable=_generate_data,
        op_kwargs=dict(n=EVENTS_PER_DAY, base_time="{{ ds }}"),
        trigger_rule = 'one_success'
    )

    check_day >> [wait_for_financial_data_completion, skip_wait]
    wait_for_financial_data_completion >> generate_data
    skip_wait >> generate_data
