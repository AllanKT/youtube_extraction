from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from datetime import datetime, timedelta

from src.tasks import *
from src.settings import *

with DAG(
    dag_id='scrap_videos',
    schedule_interval=configs.INTERVAL,
    default_args=configs.DEFAULT_ARGS,
    catchup=False,
) as dag:

    start = DummyOperator(task_id='start', dag=dag)
    scrap=PythonOperator(
        task_id='scrap',
        python_callable=scrap,
        dag=dag
    )
    end = DummyOperator(task_id='end', dag=dag)

start >> scrap
scrap >> end
