from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

def print_hello():
    return 'Hello, Airflow!'

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
}

dag = DAG(
    "example_dag",
    default_args=default_args,
    schedule=None,
)

task = PythonOperator(
    task_id='print_hello_task',
    python_callable=print_hello,
    dag=dag,
)