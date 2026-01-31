"""
DAG: курс Bitcoin (CoinGecko) → Postgres.
Таски Extract и Load, данные между ними через XCom.
Connection: postgres_default (host=db).
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from etl_btc import (
    create_table_if_missing,
    extract_data,
    get_engine,
    load_data,
)


def extract_btc():
    """Таск Extract: API → возврат в XCom."""
    return extract_data()


def load_btc(**context):
    """Таск Load: XCom → create_table → insert в crypto_prices."""
    data = context["ti"].xcom_pull(task_ids="extract_btc")
    if not data:
        return
    engine = get_engine()
    create_table_if_missing(engine)
    load_data(engine, data)


default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 1, 1),
}

dag = DAG(
    "btc_price_dag",
    default_args=default_args,
    schedule="0 * * * *",  # каждый час
    catchup=False,
    tags=["etl", "btc"],
)

extract_task = PythonOperator(
    task_id="extract_btc",
    python_callable=extract_btc,
    dag=dag,
)

load_task = PythonOperator(
    task_id="load_btc",
    python_callable=load_btc,
    dag=dag,
)

extract_task >> load_task
