def translate_text(key, lang):
    translations = {
        'uk': {
            'lang_l': 'Мова',
            'lang_name': 'Українська',
            'speed': 'Швидкість',
            'less': 'менша ніж',
            'greater': 'більша ніж',
            'equal': 'дорівнює',
            'kmh': 'км/год',
            'ms': 'м/с'
        },
        'en': {
            'lang_l': 'Language',
            'lang_name': 'English',
            'speed': 'Speed',
            'less': 'is less than',
            'greater': 'is greater than',
            'equal': 'is equal to',
            'kmh': 'km/h',
            'ms': 'm/s'
        }
    }
    if lang not in translations:
        lang = 'uk'
        
    return translations[lang].get(key, key)

def convert_and_compare_speeds(v1_kmh, v2_ms):
    v1_ms = round(v1_kmh / 3.6, 1)
    v2_kmh = round(v2_ms * 3.6, 1)
    return v1_ms, v2_kmh