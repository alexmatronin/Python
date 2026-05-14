import os

def main():
    student_surname = os.getenv("Student_Surname")

    if student_surname:
        print(f"{student_surname}")
    else:
        print("Системну змінну не знайдено.")

if __name__ == "__main__":
    main()