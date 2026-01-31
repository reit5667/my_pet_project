# Образ Airflow с зависимостями для ETL (requests, sqlalchemy, psycopg2-binary)
FROM apache/airflow:latest

COPY requirements.txt /tmp/requirements.txt
COPY entrypoint_airflow.sh /entrypoint_airflow.sh

USER root
RUN chmod +x /entrypoint_airflow.sh
USER airflow

RUN pip install --no-cache-dir -r /tmp/requirements.txt

ENTRYPOINT ["/entrypoint_airflow.sh"]
