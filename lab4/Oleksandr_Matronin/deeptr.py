from package_translator import module_3
import package_translator

print(f"Назва пакету: {package_translator.NAME}")
print(f"Автор: {package_translator.AUTHOR}")

print("Модуль 3 (deep_translator та langdetect)")

print("\n1. Функція TransLate")
txt = "Моя дівчина готує краще за всіх."
print(f"Оригінал: {txt}")
print(f"Переклад (uk -> id): {module_3.TransLate(txt, 'uk', 'id')}")

print("\n2. Функція LangDetect")
txt_detect = "Bonjour tout le monde"
print(f"Текст: {txt_detect}")
print(f"Результат ('all'): {module_3.LangDetect(txt_detect, 'all')}")

print("\n3. Функція CodeLang")
print(f"Код для 'indonesian': {module_3.CodeLang('indonesian')}")
print(f"Назва для 'id': {module_3.CodeLang('id')}")

print("\n4. Функція LanguageList")
status = module_3.LanguageList("file", "Добрий день")

print(f"\nСтатус виконання: {status}")