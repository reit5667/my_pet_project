from sqlalchemy import create_engine, text

# 1. Настройка подключения
# Формат: postgresql://пользователь:пароль@хост:порт/название_базы
DB_URL = "postgresql://admin:root@localhost:5432/analytics_db"

def main():
    print("🚀 Пробуем подключиться к базе...")
    
    # Создаем "движок" (это объект, который умеет общаться с базой)
    engine = create_engine(DB_URL)

    try:
        # Открываем соединение
        with engine.connect() as connection:
            print("✅ Успешное подключение!")

            # 2. Создаем таблицу (SQL запрос)
            create_table_query = """
            CREATE TABLE IF NOT EXISTS test_data (
                id SERIAL PRIMARY KEY,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            connection.execute(text(create_table_query))
            print("📦 Таблица 'test_data' проверена/создана.")

            # 3. Вставляем данные
            insert_query = "INSERT INTO test_data (message) VALUES ('Привет из Python!');"
            connection.execute(text(insert_query))
            connection.commit() # Важно! Подтверждаем изменения
            print("💾 Тестовая запись добавлена.")

    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()