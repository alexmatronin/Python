def translate_text(key, lang):
    translations = {
        'uk': {
            'lang_l': 'Мова',
            'lang_name': 'Українська',
            'time_l': 'Час (год хв)',
            'am_text': 'Час до обіду',
            'pm_text': 'Час після обіду',
            'incorrect_time': 'Некоректний час!'
        },
        'en': {
            'lang_l': 'Language',
            'lang_name': 'English',
            'time_l': 'Time (hr min)',
            'am_text': 'Time before noon',
            'pm_text': 'Time after noon',
            'incorrect_time': 'Incorrect time!'
        }
    }
    
    if lang not in translations:
        lang = 'uk'
        
    return translations[lang].get(key, key)

def convert_time_to_12h(hours, minutes):
    if not (0 <= hours <= 23) or not (0 <= minutes <= 59):
        return False, "", ""

    period = "pm" if hours >= 12 else "am"

    h_12 = hours % 12
    if h_12 == 0:
        h_12 = 12

    formatted_time = f"{h_12}:{minutes:02d} {period}"
    period_key = "pm_text" if hours >= 12 else "am_text"

    return True, formatted_time, period_key