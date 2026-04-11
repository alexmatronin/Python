import csv
from datetime import datetime
import matplotlib.pyplot as plt

def calculate_age(birth_date_str):
    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
    today = datetime.today().date()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def main():
    csv_filename = 'employees.csv'
    employees_data = []

    try:
        with open(csv_filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                employees_data.append(row)
        print("Ok")
    except Exception as e:
        print("Повідомлення про відсутність, або проблеми при відкритті файлу CSV, або Ok.")
        return

    gender_counts = {'Чоловіча': 0, 'Жіноча': 0}
    age_categories = ['younger_18', '18-45', '45-70', 'older_70']
    age_counts = {cat: 0 for cat in age_categories}
    gender_age_counts = {cat: {'Чоловіча': 0, 'Жіноча': 0} for cat in age_categories}

    for row in employees_data:
        gender = row['Стать']
        age = calculate_age(row['Дата народження'])

        if age < 18:
            category = 'younger_18'
        elif 18 <= age <= 45:
            category = '18-45'
        elif 45 < age <= 70:
            category = '45-70'
        else:
            category = 'older_70'

        gender_counts[gender] += 1
        age_counts[category] += 1
        gender_age_counts[category][gender] += 1

    print("\n2. Кількість співробітників чоловічої і жіночої статі.")
    for g, count in gender_counts.items():
        print(f"{g}: {count}")

    print("\n3. Кількість співробітників кожної вікової категорії.")
    for category, count in age_counts.items():
        print(f"{category}: {count}")

    print("\n4. Кількість співробітників жіночої та чоловічої статі кожної вікової категорії.")
    for category in age_categories:
        males = gender_age_counts[category]['Чоловіча']
        females = gender_age_counts[category]['Жіноча']
        print(f"Категорія {category} -> Чоловіки: {males}, Жінки: {females}")

    plt.figure("За статтю", figsize=(6, 6))
    plt.pie(gender_counts.values(), labels=gender_counts.keys(), autopct='%1.1f%%', colors=['#66b3ff', '#ff9999'])
    plt.title('Розподіл співробітників за статтю')
    plt.show()

    plt.figure("За віковими категоріями", figsize=(8, 5))
    plt.bar(age_counts.keys(), age_counts.values(), color='skyblue')
    plt.title('Кількість співробітників за віком')
    plt.xlabel('Вікова категорія')
    plt.ylabel('Кількість')
    plt.show()

    plt.figure("Стать за віком", figsize=(10, 6))
    x = range(len(age_categories))
    male_counts = [gender_age_counts[cat]['Чоловіча'] for cat in age_categories]
    female_counts = [gender_age_counts[cat]['Жіноча'] for cat in age_categories]
    
    width = 0.35
    plt.bar([i - width/2 for i in x], male_counts, width, label='Чоловіки', color='#66b3ff')
    plt.bar([i + width/2 for i in x], female_counts, width, label='Жінки', color='#ff9999')

    plt.xlabel('Вікова категорія')
    plt.ylabel('Кількість')
    plt.title('Розподіл статі у вікових категоріях')
    plt.xticks(x, age_categories)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()