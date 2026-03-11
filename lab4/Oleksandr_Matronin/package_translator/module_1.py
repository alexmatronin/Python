import asyncio
from googletrans import Translator, LANGUAGES

def TransLate(text: str, scr: str, dest: str) -> str:
    try:
        translator = Translator()
        result = asyncio.run(translator.translate(text, src=scr, dest=dest))
        return result.text
    except Exception as e:
        return f"Помилка перекладу: {e}"

def LangDetect(text: str, set: str = "all") -> str:
    try:
        translator = Translator()
        result = asyncio.run(translator.detect(text))
        
        if set == "lang":
            return result.lang
        elif set == "confidence":
            return str(result.confidence)
        else: 
            return f"Language: {result.lang}, Confidence: {result.confidence}"
    except Exception as e:
        return f"Помилка визначення мови: {e}"

def CodeLang(lang: str) -> str:
    try:
        lang_lower = lang.lower()
        if lang_lower in LANGUAGES:
            return LANGUAGES[lang_lower].capitalize()
            
        for code, name in LANGUAGES.items():
            if name.lower() == lang_lower:
                return code
        return "Мову або код не знайдено"
    except Exception as e:
        return f"Помилка: {e}"

def LanguageList(out: str = "screen", text: str = None) -> str:
    try:
        headers = ["№", "Language", "ISO-639 code"]
        if text:
            headers.append("Text")

        async def _fetch_translations():
            translator = Translator()
            rows = []
            for i, (code, name) in enumerate(LANGUAGES.items(), 1):
                row = [str(i), name.capitalize(), code]
                if text:
                    try:
                        res = await translator.translate(text, dest=code)
                        row.append(res.text)
                    except Exception:
                        row.append("Помилка (Rate limit)")
                    await asyncio.sleep(0.05)
                rows.append(row)
            return rows

        rows = asyncio.run(_fetch_translations())
            
        column_widths = [max(len(str(item)) for item in col) for col in zip(*([headers] + rows))]
        
        output_lines = []
        header_line = " | ".join(f"{item:<{column_widths[i]}}" for i, item in enumerate(headers))
        output_lines.append(header_line)
        output_lines.append("-" * len(header_line))
        
        for row in rows:
            row_line = " | ".join(f"{item:<{column_widths[i]}}" for i, item in enumerate(row))
            output_lines.append(row_line)
            
        formatted_table = "\n".join(output_lines)
        
        if out == "file":
            with open("languages_list.txt", "w", encoding="utf-8") as f:
                f.write(formatted_table)
        else:
            print(formatted_table)
            
        return "Ok"
    except Exception as e:
        return f"Помилка виводу таблиці: {e}"