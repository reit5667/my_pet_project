import requests
import time
from sqlalchemy import create_engine, text
from datetime import datetime

# Конфигурация
DB_URL = "postgresql://admin:root@localhost:5432/analytics_db"
API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

def create_table(engine):
    with engine.connect() as connection:
        connection.execute(text("DROP TABLE IF EXISTS crypto_prices;"))
        create_query = """
        CREATE TABLE IF NOT EXISTS crypto_prices (
            id SERIAL PRIMARY KEY,
            currency VARCHAR(50),
            price NUMERIC(10, 2),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        connection.execute(text(create_query))
        connection.commit()
        print("✅ Таблица crypto_prices готова.")

def extract_data() -> dict:
    """Этап Extract: Получаем данные из API."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status() # Если сайт упал - выдаст ошибку
        data = response.json()
        
        # API возвращает: {'bitcoin': {'usd': 95123.45}}
        price = data['bitcoin']['usd']
        print(f"💰 Текущая цена Bitcoin: ${price}")
        return {'currency': 'bitcoin', 'price': price}
    except Exception as e:
        print(f"❌ Ошибка при скачивании данных: {e}")
        return None

def load_data(engine, data: dict):
    """Этап Load: Загружаем данные в Postgres."""
    if not data:
        return

    insert_query = text("""
        INSERT INTO crypto_prices (currency, price) 
        VALUES (:currency, :price)
    """)
    
    with engine.connect() as connection:
        connection.execute(insert_query, {"currency": data['currency'], "price": data['price']})
        connection.commit()
        print("💾 Данные сохранены в БД.")

def main():
    engine = create_engine(DB_URL)
    
    # 1. Подготовка БД (выполняется один раз)
    create_table(engine)
    
    # 2. Эмуляция работы (как будто запускаем раз в минуту)
    print("🚀 Запуск мини-ETL процесса...")
    
    # Сделаем 3 цикла загрузки для теста
    for _ in range(3):
        data = extract_data()
        load_data(engine, data)
        time.sleep(2) # Пауза 2 секунды между запросами

if __name__ == "__main__":
    main()