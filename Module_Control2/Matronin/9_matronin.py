def main():
    coefficients = [-2, 2, 0, -1, 1, 2, 7]

    print(f"{len(coefficients)} коефіцієнтів полінома:")
    print(" ".join(map(str, coefficients)))

    x_str = input("Введіть дійсне число х: ")
    
    try:
        x = float(x_str.replace(',', '.'))
    except ValueError:
        print("Помилка вводу.")
        return

    result = 0.0
    n = len(coefficients) - 1 
    
    for i in range(len(coefficients)):
        power = n - i  
        result += coefficients[i] * (x ** power)

    if result > 2000000000:
        print("Переповнення!")
    else:
        formatted_result = f"{result:.2f}".replace('.', ',')
        print(f"P({x_str})={formatted_result}")

if __name__ == "__main__":
    main()