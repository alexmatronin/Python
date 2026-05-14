import psycopg2

db_params = {
    "host": "localhost",
    "port": "5433",
    "database": "telephone_station",
    "user": "postgres",
    "password": "password"
}

def print_table(cursor, title):
    print(f"\n{'='*7} {title} {'='*7}")    
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    
    if not data:
        print("Немає даних.")
        return

    col_widths = [len(col) for col in columns]
    for row in data:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    format_str = " | ".join([f"{{:<{w}}}" for w in col_widths])

    separator = "-" * (sum(col_widths) + 3 * len(columns) - 1)
    print(separator)
    print(format_str.format(*columns))
    print(separator)

    for row in data:
        print(format_str.format(*[str(cell) if cell is not None else 'NULL' for cell in row]))
    print(separator)


try:
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cursor:
            tables = ['clients', 'phones', 'tariffs', 'calls']
            for table in tables:
                cursor.execute(f"SELECT * FROM {table};")
                print_table(cursor, f"ТАБЛИЦЯ: {table.upper()}")

            query1 = """
            SELECT 
                client_code AS "Код клієнта", 
                client_type AS "Тип клієнта", 
                last_name AS "Прізвище", 
                first_name AS "Ім'я"
            FROM clients 
            WHERE client_type = 'фізична особа' 
            ORDER BY last_name;
            """
            cursor.execute(query1)
            print_table(cursor, "Запит 1: Фізичні особи (відсортовано за прізвищем)")

            query2 = """
            SELECT 
                client_type AS "Тип клієнта", 
                COUNT(*) AS "Кількість" 
            FROM clients 
            GROUP BY client_type;
            """
            cursor.execute(query2)
            print_table(cursor, "Запит 2: Кількість клієнтів за типами")

            query3 = """
            SELECT 
                c.call_code AS "Код розмови", 
                c.call_date AS "Дата", 
                c.phone_number AS "Номер телефону", 
                c.minutes_amount AS "Хвилини", 
                t.cost_per_minute AS "Тариф",
                ROUND((c.minutes_amount * t.cost_per_minute)::numeric, 2) AS "Вартість розмови"
            FROM calls c
            JOIN tariffs t ON c.tariff_code = t.tariff_code;
            """
            cursor.execute(query3)
            print_table(cursor, "Запит 3: Вартість кожної розмови")

            target_call_type = 'міжміський'
            query4 = """
            SELECT 
                c.call_code AS "Код розмови", 
                c.call_date AS "Дата", 
                c.phone_number AS "Номер телефону", 
                c.minutes_amount AS "Хвилини", 
                t.call_type AS "Тип дзвінка"
            FROM calls c
            JOIN tariffs t ON c.tariff_code = t.tariff_code
            WHERE t.call_type = %s;
            """
            cursor.execute(query4, (target_call_type,)) 
            print_table(cursor, f"Запит 4: Розмови за типом '{target_call_type}'")

            query5 = """
            SELECT 
                cl.last_name AS "Прізвище", 
                cl.first_name AS "Ім'я",
                ROUND(SUM(c.minutes_amount * t.cost_per_minute)::numeric, 2) AS "Загальна сума витрат"
            FROM clients cl
            JOIN phones p ON cl.client_code = p.client_code
            JOIN calls c ON p.phone_number = c.phone_number
            JOIN tariffs t ON c.tariff_code = t.tariff_code
            GROUP BY cl.client_code, cl.last_name, cl.first_name
            ORDER BY "Загальна сума витрат" DESC;
            """
            cursor.execute(query5)
            print_table(cursor, "Запит 5: Загальна вартість всіх розмов кожного клієнта")

            query6 = """
            SELECT 
                cl.last_name AS "Прізвище",
                SUM(CASE WHEN t.call_type = 'внутрішній' THEN c.minutes_amount ELSE 0 END) AS "Внутрішні (хв)",
                SUM(CASE WHEN t.call_type = 'міжміський' THEN c.minutes_amount ELSE 0 END) AS "Міжміські (хв)",
                SUM(CASE WHEN t.call_type = 'мобільний' THEN c.minutes_amount ELSE 0 END) AS "Мобільні (хв)"
            FROM clients cl
            JOIN phones p ON cl.client_code = p.client_code
            JOIN calls c ON p.phone_number = c.phone_number
            JOIN tariffs t ON c.tariff_code = t.tariff_code
            GROUP BY cl.client_code, cl.last_name
            ORDER BY cl.last_name;
            """
            cursor.execute(query6)
            print_table(cursor, "Запит 6: Кількість хвилин кожного типу дзвінків для кожного клієнта")

except psycopg2.Error as e:
    print(f"Помилка при виконанні запитів: {e}")