import asyncio
import time
import os
import re
from googletrans import Translator, LANGUAGES, LANGCODES

translator = Translator()

async def TransLate(str, lang):
    try:
        transl = lang.lower()
        if transl in LANGCODES:
            code = LANGCODES[transl]
        elif transl in LANGUAGES:
            code = transl
        else:
            return f"Мову '{lang}' не знайдено."
        
        result = await translator.translate(str, dest=code)
        return result.text
    except Exception as e:
        return f"Помилка перекладу: {e}"

async def LangDetect(txt):
    try:
        result = await translator.detect(txt)
        return result.lang, result.confidence
    except Exception as e:
        return "Error", 0.0

def CodeLang(lang):
    transl = lang.lower()
    if transl in LANGUAGES:
        return LANGUAGES[transl].capitalize()
    elif transl in LANGCODES:
        return LANGCODES[transl]
    return "Error"

async def main():
    file_name = "Steve_Jobs.txt"
    transl_lang = "indonesian" 
    
    if not os.path.exists(file_name):
        print(f"Файл {file_name} не знайдено.")
        return

    with open(file_name, 'r', encoding='utf-8') as file:
        original_text = file.read()

    char_count = len(original_text)
    
    TxtList = re.split(r'(?<=[.!?])\s+', original_text.strip())
    TxtList = [s for s in TxtList if s]
    sentence_count = len(TxtList)

    start_sync = time.time()
    
    orig_lang_code, confidence = await LangDetect(original_text)
    
    translated_sync_list = []
    for sentence in TxtList:
        tr_text = await TransLate(sentence, transl_lang)
        translated_sync_list.append(tr_text)
        
    sync_time = time.time() - start_sync
    translated_text_sync = " ".join(translated_sync_list)

    start_async = time.time()
    
    detect_task = asyncio.create_task(LangDetect(original_text))
    translate_tasks = [asyncio.create_task(TransLate(s, transl_lang)) for s in TxtList]
    
    await detect_task
    translated_async_list = await asyncio.gather(*translate_tasks)
    
    async_time = time.time() - start_async

    orig_lang_name = CodeLang(orig_lang_code)
    transl_lang_code = CodeLang(transl_lang)

    print(f"\nІм'я файлу: {file_name}")
    print(f"Кількість символів: {char_count}")
    print(f"Кількість речень: {sentence_count}")
    print(f"Оригінальна мова: {orig_lang_name}, код: {orig_lang_code}, confidence: {confidence}")
    print(f"\nОригінальний текст:\n{original_text}\n")
    print(f"Мова перекладу: {transl_lang.capitalize()}, код: {transl_lang_code}")
    print(f"\nПереклад тексту на індонезійську:\n{translated_text_sync}\n")
    print(f"Час, затрачений на визначення мови та перекладу (пункт 3.4.1): {sync_time:.4f} сек")
    print(f"Час, затрачений на визначення мови та перекладу в асинхроному режимі (пункт 3.4.2): {async_time:.4f} сек\n")

if __name__ == "__main__":
    asyncio.run(main())