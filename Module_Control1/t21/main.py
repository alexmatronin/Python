import json
import os
import sys
from fc import translate_text, calculate_time_to_midnight

DATA_FILE = "MyData.json"

def create_data_file():
    try:
        time_input = input("Введіть час (ч м): ")
        parts = time_input.strip().split()
        
        if len(parts) != 2:
            raise ValueError("Потрібно ввести два числа.")

        h = int(parts[0])
        m = int(parts[1])
        period = input("Введіть половину доби: ").strip().lower()
        lang = input("Введіть мову інтерфейсу: ").strip().lower()
        
        data = {
            "hours": h,
            "minutes": m,
            "period": period,
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
        period = str(data['period']).strip().lower()
        lang = str(data['lang']).strip().lower()
    except (json.JSONDecodeError, KeyError, ValueError):
        create_data_file()
        sys.exit()

    if lang not in ['uk', 'en']:
        lang = 'uk'

    lang_l = translate_text('lang_l', lang)
    lang_name = translate_text('lang_name', lang)
    time_l = translate_text('time_l', lang)
    period_l = translate_text('period_l', lang)
    incorrect_time = translate_text('incorrect_time', lang)

    print(f"{lang_l}: {lang_name}")
    print(f"{time_l}: {h} {m}")
    print(f"{period_l}: {period}")

    is_valid, left_h, left_m = calculate_time_to_midnight(h, m, period)

    if not is_valid:
        print(incorrect_time)
    else:
        time_left_t = translate_text('time_left', lang)
        print(time_left_t.format(h=left_h, m=left_m))

if __name__ == "__main__":
    main()