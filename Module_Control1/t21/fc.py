def translate_text(key, lang):
    translations = {
        'uk': {
            'lang_l': 'Мова',
            'lang_name': 'Українська',
            'time_l': 'Час (ч м)',
            'period_l': 'Половина доби',
            'incorrect_time': 'Некоректний час!',
            'time_left': 'До опівночі залишилося {h} годин {m} хвилин.'
        },
        'en': {
            'lang_l': 'Language',
            'lang_name': 'English',
            'time_l': 'Time (h m)',
            'period_l': 'Half of the day',
            'incorrect_time': 'Incorrect time!',
            'time_left': '{h} hours {m} minutes left until midnight.'
        }
    }
    
    if lang not in translations:
        lang = 'uk'
        
    return translations[lang].get(key, key)

def calculate_time_to_midnight(hours, minutes, period):
    if not (1 <= hours <= 12) or not (0 <= minutes <= 59) or period not in ['a', 'p']:
        return False, 0, 0
    
    if period == 'a':
        h_24 = 0 if hours == 12 else hours
    else: # period == 'p'
        h_24 = 12 if hours == 12 else hours + 12

    current_total_minutes = h_24 * 60 + minutes
    minutes_in_day = 24 * 60
    minutes_left = minutes_in_day - current_total_minutes
    
    left_h = minutes_left // 60
    left_m = minutes_left % 60

    if left_h == 24:
        left_h = 0

    return True, left_h, left_m