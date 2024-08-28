def addition(a, b):
    try: 
        return a + b
    except (TypeError, ValueError):
        return "Please enter valid numeric values"

def subtract(a, b):
    try: 
        return a - b
    except (TypeError, ValueError):
        return "Please enter valid numeric values"

def multiply(a, b):
    try: 
        return a * b
    except (TypeError, ValueError):
        return "Please enter valid numeric values"

def division(a, b):
    try:
        if b == 0:
            raise ZeroDivisionError
        return a / b
    except (ZeroDivisionError, TypeError, ValueError):
        return "Invalid operation: division by zero or non-numeric input"

def calculator():
    operation = input("Enter operation (+, -, *, /): ")
    while True:
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            if operation == '+':
                result = addition(num1, num2)
            elif operation == '-':
                result = subtract(num1, num2)
            elif operation == '*':
                result = multiply(num1, num2)
            elif operation == '/':
                result = division(num1, num2)
            else:
                result = "Invalid operation"
            print("Result:", result)
        except ValueError:
            print("Invalid input. Please enter numeric values.")

calculator()