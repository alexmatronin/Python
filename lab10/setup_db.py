import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from faker import Faker
import random
from datetime import date, timedelta

db_params_default = {
    "host": "localhost",
    "port": "5433",
    "database": "postgres",
    "user": "postgres",
    "password": "password"
}

try:
    conn = psycopg2.connect(**db_params_default)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE telephone_station;")
    cursor.close()
    conn.close()
    print("Базу даних 'telephone_station' успішно створено.")
except psycopg2.Error as e:
    print(f"БД вже існує: {e}")

db_params = {
    "host": "localhost",
    "port": "5433",
    "database": "telephone_station",
    "user": "postgres",
    "password": "password"
}

try:
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        client_code SERIAL PRIMARY KEY,
        client_type VARCHAR(50) CHECK (client_type IN ('відомство', 'фізична особа')),
        address TEXT,
        last_name VARCHAR(100),
        first_name VARCHAR(100),
        patronymic VARCHAR(100)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS phones (
        phone_number VARCHAR(20) PRIMARY KEY,
        client_code INTEGER REFERENCES clients(client_code)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tariffs (
        tariff_code SERIAL PRIMARY KEY,
        call_type VARCHAR(50) CHECK (call_type IN ('внутрішній', 'міжміський', 'мобільний')),
        cost_per_minute REAL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calls (
        call_code SERIAL PRIMARY KEY,
        call_date DATE,
        phone_number VARCHAR(20) REFERENCES phones(phone_number),
        minutes_amount INTEGER,
        tariff_code INTEGER REFERENCES tariffs(tariff_code)
    );
    """)
    conn.commit()

    fake = Faker('uk_UA')

    cursor.execute("TRUNCATE TABLE calls, tariffs, phones, clients RESTART IDENTITY CASCADE;")
    
    # 5 клієнтів
    client_types = ['відомство', 'фізична особа']
    client_ids = []
    for _ in range(5):
        cursor.execute(
            "INSERT INTO clients (client_type, address, last_name, first_name, patronymic) VALUES (%s, %s, %s, %s, %s) RETURNING client_code",
            (random.choice(client_types), fake.address(), fake.last_name(), fake.first_name(), fake.middle_name())
        )
        client_ids.append(cursor.fetchone()[0])

    phones_data = []
    for _ in range(7):
        phones_data.append((fake.phone_number(), random.choice(client_ids)))
    cursor.executemany("INSERT INTO phones (phone_number, client_code) VALUES (%s, %s)", phones_data)

    tariffs_data = [
        ('внутрішній', 0.50),
        ('міжміський', 2.00),
        ('мобільний', 1.20)
    ]
    tariff_ids = []
    for data in tariffs_data:
        cursor.execute("INSERT INTO tariffs (call_type, cost_per_minute) VALUES (%s, %s) RETURNING tariff_code", data)
        tariff_ids.append(cursor.fetchone()[0])

    start_date = date(2026, 5, 1)
    calls_data = []
    for _ in range(20):
        random_day = random.randint(0, 30)
        call_date = start_date + timedelta(days=random_day)
        random_phone = random.choice(phones_data)[0]
        random_tariff = random.choice(tariff_ids)
        duration = random.randint(1, 60)
        
        calls_data.append((
            call_date,
            random_phone,
            duration,
            random_tariff
        ))
    cursor.executemany(
        "INSERT INTO calls (call_date, phone_number, minutes_amount, tariff_code) VALUES (%s, %s, %s, %s)",
        calls_data
    )

    conn.commit()
    print("Таблиці створено та заповнено даними")

    cursor.close()
    conn.close()

except psycopg2.Error as e:
    print(f"Помилка роботи з базою даних: {e}")