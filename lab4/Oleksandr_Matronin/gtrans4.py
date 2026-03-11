from package_translator import module_1
import package_translator

print(f"\nНазва пакету: {package_translator.NAME}")
print(f"Автор: {package_translator.AUTHOR}")
print("\nМодуль 1 (googletrans 4.0.2)")


print("\n1. Функція TransLate")
txt = "Моя дівчина готує краще за всіх."
print(f"Оригінал: {txt}")
print(f"Переклад (uk -> en): {module_1.TransLate(txt, 'uk', 'en')}")
print(f"Переклад (uk -> id): {module_1.TransLate(txt, 'uk', 'id')}")

print("\n2. Функція LangDetect")
txt_detect = "Guten Tag"
print(f"Текст: {txt_detect}")
print(f"Параметр 'all': {module_1.LangDetect(txt_detect, 'all')}")
print(f"Параметр 'lang': {module_1.LangDetect(txt_detect, 'lang')}")
print(f"Параметр 'confidence': {module_1.LangDetect(txt_detect, 'confidence')}")

print("\n3. Функція CodeLang")
print(f"Назва 'ukrainian': {module_1.CodeLang('ukrainian')}")
print(f"Код 'de': {module_1.CodeLang('de')}")
print(f"Назва з помилкою 'qwerty': {module_1.CodeLang('qwerty')}")

print("\n4. Функція LanguageList")
print("LanguageList('file', 'Добрий день')\n")

status = module_1.LanguageList("file", "Добрий день")
print(f"\nСтатус виконання: {status}")