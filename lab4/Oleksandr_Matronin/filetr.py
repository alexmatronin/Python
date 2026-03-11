import os
import re
import json 
from package_translator import module_1, module_2, module_3

def count_sentences(text: str) -> int:
    sentences = re.findall(r'[^\.!\?]+[\.!\?]+', text)
    return len(sentences)

def get_sentences(text: str, limit: int) -> str:
    sentences = re.findall(r'[^\.!\?]+[\.!\?]+', text)
    selected = sentences[:limit]
    return " ".join(s.strip() for s in selected)

def read_config(config_file="config.json"):
    with open(config_file, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
        
    return (
        config_data.get("file_name"),
        config_data.get("target_lang"),
        config_data.get("module_name"),
        config_data.get("output_dest"),
        config_data.get("sentences_count")
    )

def main():
    try:
        file_name, target_lang, module_name, output_dest, limit_sentences = read_config()
    except Exception as e:
        print(f"Помилка читання конфігураційного файлу config.json: {e}")
        return
    
    if not os.path.exists(file_name):
        print(f"Файл '{file_name}' не знайдено.")
        return

    if module_name == "module_1":
        translator = module_1
    elif module_name == "module_2":
        translator = module_2
    elif module_name == "module_3":
        translator = module_3
    else:
        print(f"Невідомий модуль '{module_name}'")
        return

    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            full_text = f.read()
    except Exception as e:
        print(f"Помилка читання файлу: {e}")
        return

    if not full_text.strip():
        print("Файл з текстом порожній.")
        return

    file_size = os.path.getsize(file_name)
    total_chars = len(full_text)
    total_sentences = count_sentences(full_text)

    detect_res = translator.LangDetect(full_text, "lang")
    if "Помилка" in detect_res:
        orig_lang_name = "Невідомо"
    else:
        orig_lang_name = translator.CodeLang(detect_res)

    print(f"\nНазва файлу: {file_name}")
    print(f"Розмір файлу: {file_size} байт")
    print(f"Кількість символів: {total_chars}")
    print(f"Кількість речень: {total_sentences}")
    print(f"Мова тексту: {orig_lang_name}")

    text_to_translate = get_sentences(full_text, limit_sentences)

    translated_text = translator.TransLate(text_to_translate, "auto", target_lang)
    
    if "Помилка" in translated_text:
        print(translated_text)
        return

    target_lang_name = translator.CodeLang(target_lang)

    if output_dest.lower() == "screen":
        print(f"\nМова перекладу: {target_lang_name}")
        print(f"Використаний модуль: {module_name}")

        print(f"\nОригінальний текст ({limit_sentences})")
        print(text_to_translate)    

        print(f"\nПерекладений текст:\n{translated_text}")
        
    elif output_dest.lower() == "file":
        try:
            base_name, ext = os.path.splitext(file_name)
            res_file = f"{base_name}_{target_lang}{ext}"
            
            with open(res_file, "w", encoding="utf-8") as f:
                f.write(translated_text)
            print("Ok")
        except Exception as e:
            print(f"Помилка запису у файл: {e}")
    else:
        print(f"Невідомий параметр виводу '{output_dest}' у конфігураційному файлі.")

if __name__ == "__main__":
    main()