import json
import os
import sys
from fc import translate_text, convert_and_compare_speeds

DATA_FILE = "MyData.json"

def create_data_file():
    try:
        v1 = float(input("Введіть швидкість v1 (км/год): "))
        v2 = float(input("Введіть швидкість v2 (м/с): "))
        lang = input("Введіть мову інтерфейсу: ")
        
        data = {
            "v1": v1,
            "v2": v2,
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
            
        v1 = float(data['v1'])
        v2 = float(data['v2'])
        lang = str(data['lang']).strip().lower()
    except (json.JSONDecodeError, KeyError, ValueError):
        create_data_file()
        sys.exit()

    if lang not in ['uk', 'en']:
        lang = 'uk'

    lang_l = translate_text('lang_l', lang)
    lang_name = translate_text('lang_name', lang)
    speed_str = translate_text('speed', lang)
    kmh_str = translate_text('kmh', lang)
    ms_str = translate_text('ms', lang)
    
    v1_ms, v2_kmh = convert_and_compare_speeds(v1, v2)

    if v1_ms < v2:
        comp_str = translate_text('less', lang)
    elif v1_ms > v2:
        comp_str = translate_text('greater', lang)
    else:
        comp_str = translate_text('equal', lang)

    def fmt(num):
        formatted = f"{num:g}"
        if lang == 'uk':
            formatted = formatted.replace('.', ',')
        return formatted

    print(f"{lang_l}: {lang_name}")
    print(f"{speed_str} v1 ({kmh_str}) {fmt(v1)}")
    print(f"{speed_str} v2 ({ms_str}) {fmt(v2)}")
    print(f"{speed_str} {fmt(v1)} {kmh_str} = {fmt(v1_ms)} {ms_str}")
    print(f"{speed_str} {fmt(v2)} {ms_str} = {fmt(v2_kmh)} {kmh_str}")
    print(f"{speed_str} v1={fmt(v1)} {kmh_str}, {comp_str} {speed_str.lower()} v2={fmt(v2)}{ms_str}")

if __name__ == "__main__":
    main()