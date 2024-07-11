from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
import pendulum
import datetime
from td7.data_generator import DataGenerator
from td7.schema import Schema

def _load_dollar_blue_data(base_time: str):
    generator = DataGenerator()
    schema = Schema()

    end_date = datetime.datetime.fromisoformat(base_time)
    start_date = end_date - datetime.timedelta(days=7)
    last_week_data = generator.load_dollar_blue_data(start_date, end_date)

    schema.insert(last_week_data, "dollarblue")


def _total_bets_last_week():
    schema = Schema()
    total_bet = int(schema.get_last_week_total_bet()[0]['total_apuesta'])

    if total_bet > 1000000000000:
        return 'trigger_internal_external_report'
    else:
        return 'trigger_internal_report'


with DAG(
    "financial_data",
    start_date=pendulum.datetime(2024, 6, 1, tz="UTC"),
    schedule_interval="@weekly",
    catchup=True,
) as dag:

    dollar_blue_data = PythonOperator(
        task_id="dollar_blue_data",
        python_callable=_load_dollar_blue_data,
        op_kwargs=dict(base_time="{{ ds }}"),
    )

    bets_branch = BranchPythonOperator(
        task_id="get_bets_branch",
        python_callable=_total_bets_last_week,
        op_kwargs=dict(base_time="{{ ds }}"),
    )

    trigger_A = TriggerDagRunOperator(
        task_id="trigger_internal_external_report",
        trigger_dag_id="dbt_external_reporting", 
        conf={"message": "external & internal"},
    )

    trigger_B = TriggerDagRunOperator(
        task_id="trigger_internal_report",
        trigger_dag_id="dbt_internal_use", 
        conf={"message": "only internal"},
    )
    
    dollar_blue_data >> bets_branch >> [trigger_A, trigger_B]

