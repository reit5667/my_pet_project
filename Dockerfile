# Образ Airflow с зависимостями для ETL (requests, sqlalchemy, psycopg2-binary)
FROM apache/airflow:latest

COPY requirements.txt /tmp/requirements.txt

# В образе apache/airflow пакеты нужно ставить от пользователя airflow, не от root
USER airflow
RUN pip install --no-cache-dir -r /tmp/requirements.txt
