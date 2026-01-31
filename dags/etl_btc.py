"""
ETL-функции для курса Bitcoin (CoinGecko API) → Postgres.
Подключение к БД через Airflow Connection (host=db в Docker).
"""
from urllib.parse import quote_plus

import requests
from sqlalchemy import create_engine, text
from airflow.hooks.base import BaseHook

API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"


def get_engine(conn_id: str = "postgres_default"):
    """Создаёт SQLAlchemy engine из Airflow Connection (host=db:5432 в Docker)."""
    conn = BaseHook.get_connection(conn_id)
    # schema в Postgres Connection = имя БД
    password = quote_plus(conn.password) if conn.password else ""
    uri = (
        f"postgresql+psycopg2://{conn.login}:{password}@{conn.host}:{conn.port}/{conn.schema}"
    )
    return create_engine(uri)


def create_table_if_missing(engine):
    """Создаёт таблицу crypto_prices при отсутствии (без DROP — для периодического DAG)."""
    with engine.connect() as connection:
        connection.execute(
            text("""
                CREATE TABLE IF NOT EXISTS crypto_prices (
                    id SERIAL PRIMARY KEY,
                    currency VARCHAR(50),
                    price NUMERIC(10, 2),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        )
        connection.commit()


def extract_data() -> dict:
    """Extract: запрос к CoinGecko API, возвращает {'currency': 'bitcoin', 'price': float}."""
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    price = data["bitcoin"]["usd"]
    return {"currency": "bitcoin", "price": price}


def load_data(engine, data: dict) -> None:
    """Load: вставка одной записи в crypto_prices."""
    if not data:
        return
    with engine.connect() as connection:
        connection.execute(
            text(
                "INSERT INTO crypto_prices (currency, price) VALUES (:currency, :price)"
            ),
            {"currency": data["currency"], "price": data["price"]},
        )
        connection.commit()
