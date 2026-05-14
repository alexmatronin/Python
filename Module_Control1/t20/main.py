import json
import os
import sys
from fc import translate_text, convert_time_to_12h

DATA_FILE = "MyData.json"

def create_data_file():
    try:
        time_input = input("Введіть час (год хв): ")
        parts = time_input.strip().split()
        
        if len(parts) != 2:
            raise ValueError("Потрібно ввести два числа.")

        h = int(parts[0])
        m = int(parts[1])
        lang = input("Введіть мову інтерфейсу: ")
        
        data = {
            "hours": h,
            "minutes": m,
            "lang": lang
        }
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"Дані збережено в файл {DATA_FILE}")
    except ValueError:
        print("Помилка вводу.")

def main():
    if not os.path.exists(DATA_FILE):
        create_data_file()
        sys.exit()
        
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        h = int(data['hours'])
        m = int(data['minutes'])
        lang = str(data['lang']).strip().lower()
    except (json.JSONDecodeError, KeyError, ValueError):
        create_data_file()
        sys.exit()

    if lang not in ['uk', 'en']:
        lang = 'uk'

    lang_l = translate_text('lang_l', lang)
    lang_name = translate_text('lang_name', lang)
    time_l = translate_text('time_l', lang)
    incorrect_time = translate_text('incorrect_time', lang)

    print(f"{lang_l}: {lang_name}")
    print(f"{time_l}: {h} {m}")

    is_valid, formatted_time, period_key = convert_time_to_12h(h, m)

    if not is_valid:
        print(incorrect_time)
    else:
        period_text = translate_text(period_key, lang)
        print(formatted_time)
        print(period_text)

if __name__ == "__main__":
    main()