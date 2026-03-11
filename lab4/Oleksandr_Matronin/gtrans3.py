from package_translator import module_2
import package_translator

print(f"\nНазва пакету: {package_translator.NAME}")
print(f"Автор: {package_translator.AUTHOR}")
print("\nМодуль 2 (googletrans 3.1.0a0)")

print("\n1. Функція TransLate")
txt = "Моя дівчина готує краще за всіх."
print(f"Оригінал: {txt}")
print(f"Переклад (uk -> id): {module_2.TransLate(txt, 'uk', 'id')}")

print("\n2. Функція LangDetect")
print(module_2.LangDetect("Guten Tag", "all"))

print("\n3. Функція CodeLang")
print(f"Код для 'indonesian': {module_2.CodeLang('indonesian')}")

print("\n4. Функція LanguageList")
print("Таблиця для виводу списку мов:")

print(module_2.LanguageList("file", "Добрий день"))