import csv
import random
from datetime import date
from faker import Faker

fake = Faker(locale='uk_UA')

patronymics = {
    'Чоловічі': [
        'Олександрович', 'Миколайович', 'Володимирович', 'Іванович', 'Петрович',
        'Васильович', 'Михайлович', 'Анатолійович', 'Вікторович', 'Сергійович',
        'Юрійович', 'Олексійович', 'Павлович', 'Андрійович', 'Степанович',
        'Григорович', 'Романович', 'Дмитрович', 'Богданович', 'Тарасович'
    ],
    'Жіночі': [
        'Олександрівна', 'Миколаївна', 'Володимирівна', 'Іванівна', 'Петрівна',
        'Василівна', 'Михайлівна', 'Анатоліївна', 'Вікторівна', 'Сергіївна',
        'Юріївна', 'Олексіївна', 'Павлівна', 'Андріївна', 'Степанівна',
        'Григорівна', 'Романівна', 'Дмитрівна', 'Богданівна', 'Тарасівна'
    ]
}

def generate_employees(total_count=500):
    female_count = int(total_count * 0.4)
    male_count = total_count - female_count
    
    genders = ['Жіноча'] * female_count + ['Чоловіча'] * male_count
    random.shuffle(genders)
    
    employees = []
    for gender in genders:
        if gender == 'Жіноча':
            last_name = fake.last_name_female()
            first_name = fake.first_name_female()
            patronymic = random.choice(patronymics['Жіночі'])
        else:
            last_name = fake.last_name_male()
            first_name = fake.first_name_male()
            patronymic = random.choice(patronymics['Чоловічі'])

        birth_date = fake.date_between(start_date=date(1946, 1, 1), end_date=date(2011, 12, 31))

        job = fake.job()
        city = fake.city()
   
        address = fake.address().replace('\n', ', ')
        phone = fake.phone_number()
        email = fake.email()

        employees.append({
            'Прізвище': last_name,
            'Ім\'я': first_name,
            'По батькові': patronymic,
            'Стать': gender,
            'Дата народження': birth_date.strftime('%Y-%m-%d'),
            'Посада': job,
            'Місто проживання': city,
            'Адреса проживання': address,
            'Телефон': phone,
            'Email': email
        })
        
    return employees

def save_csv(data, filename='employees.csv'):
    fieldnames = [
        'Прізвище', 'Ім\'я', 'По батькові', 'Стать', 'Дата народження',
        'Посада', 'Місто проживання', 'Адреса проживання', 'Телефон', 'Email'
    ]

    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader() 
        writer.writerows(data) 

if __name__ == "__main__":
    employees_data = generate_employees(500)
    save_csv(employees_data)
    print("Файл employees.csv створено та заповнено.")