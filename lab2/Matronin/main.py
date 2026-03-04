from googletrans import Translator, LANGUAGES, LANGCODES

translator = Translator()


def CodeLang(lang: str):
    target  = lang.lower()

    if target  in LANGUAGES:     
        return LANGUAGES[target ].capitalize()
    elif target  in LANGCODES:  
        return LANGCODES[target ]
    return None


def TransLate(text: str, lang: str) -> str:
    try:
        target  = lang.lower()

        if target  in LANGCODES:    
            code = LANGCODES[target ]
        elif target  in LANGUAGES:   
            code = target 
        else:
            return f"Помилка: мову '{lang}' не знайдено."

        result = translator.translate(text, dest=code)
        return result.text
    except Exception as e:
        return f"Помилка перекладу: {e}"


def LangDetect(txt: str) -> str:
    try:
        detected = translator.detect(txt)
        return f"Detected(lang={detected.lang}, confidence={detected.confidence})"
    except Exception as e:
        return f"Помилка визначення мови: {e}"

if __name__ == "__main__":
    txt = input("Введіть текст для перекладу:\n> ")
    lang = input("Введіть мову (код 'en' або назву 'english'):\n> ")

    print()
    print(f"Текст: {txt}")
    print(f"Мова: {LangDetect(txt)}")
    print(f"Переклад: {TransLate(txt, lang)}")
    print(f"CodeLang: {CodeLang(lang)}")