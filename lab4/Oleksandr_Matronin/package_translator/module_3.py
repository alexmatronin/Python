from deep_translator import GoogleTranslator
from langdetect import detect, detect_langs, DetectorFactory

DetectorFactory.seed = 0

def TransLate(text: str, scr: str, dest: str) -> str:
    try:
        translator = GoogleTranslator(source=scr, target=dest)
        return translator.translate(text)
    except Exception as e:
        return f"Помилка перекладу: {e}"

def LangDetect(text: str, set: str = "all") -> str:
    try:
        result = detect_langs(text)[0]
        lang_code = result.lang
        confidence = result.prob
        
        if set == "lang":
            return lang_code
        elif set == "confidence":
            return str(confidence)
        else: 
            return f"Language: {lang_code}, Confidence: {confidence}"
    except Exception as e:
        return f"Помилка визначення мови: {e}"

def CodeLang(lang: str) -> str:
    try:
        langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
        lang_lower = lang.lower()

        if lang_lower in langs_dict:
            return langs_dict[lang_lower]
    
        for name, code in langs_dict.items():
            if code == lang_lower:
                return name.capitalize()
                
        return "Мову або код не знайдено"
    except Exception as e:
        return f"Помилка: {e}"

def LanguageList(out: str = "screen", text: str = None) -> str:
    try:
        langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
        headers = ["№", "Language", "ISO-639 code"]
        if text:
            headers.append("Text")
            
        rows = []
        for i, (name, code) in enumerate(langs_dict.items(), 1):
            row = [str(i), name.capitalize(), code]
            if text:
                try:
                    res = GoogleTranslator(source='auto', target=code).translate(text)
                    row.append(res)
                except:
                    row.append("Помилка")
            rows.append(row)
            
        col_widths = [max(len(str(item)) for item in col) for col in zip(*([headers] + rows))]
        
        output_lines = []
        header_line = " | ".join(f"{item:<{col_widths[i]}}" for i, item in enumerate(headers))
        output_lines.append(header_line)
        output_lines.append("-" * len(header_line))
        
        for row in rows:
            row_line = " | ".join(f"{item:<{col_widths[i]}}" for i, item in enumerate(row))
            output_lines.append(row_line)
            
        formatted_table = "\n".join(output_lines)
        
        if out == "file":
            with open("languages_list_module_3.txt", "w", encoding="utf-8") as f:
                f.write(formatted_table)
        else:
            print(formatted_table)
            
        return "Ok"
    except Exception as e:
        return f"Помилка виводу таблиці: {e}"