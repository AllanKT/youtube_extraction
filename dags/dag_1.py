from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'airflow',
    'dependes_on_past': False,
    'start_date': datetime(2021, 10, 9),
    'retries': 0
}

# gerenciador de contexto
# cron expression "0/5 * * * *"
with DAG(dag_id='DAG-1', default_args=default_args, catchup=False, schedule_interval='@once') as dag:
    start = DummyOperator(task_id='start', dag=dag)
    end = DummyOperator(task_id='end', dag=dag)

start >> end
