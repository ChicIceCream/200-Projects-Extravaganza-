def addition(a, b):
    try: 
        if a + b == True:
            return a + b
    except ValueError:
        return "Please enter the correct values"

def substract(a, b):
    try: 
        if a - b == True:
            return a - b
    except ValueError:
        return "Please enter the correct values"

def multiply(a, b):
    try: 
        if a * b == True:
            return a * b
    except ValueError:
        return "Please enter the correct values"

def division(a, b):
    try: 
        if a / b == True:
            return a / b
    except ValueError:
        return "Please enter the correct values"
    except ZeroDivisionError:
        return "Do not divide by 0"

print(division(3, "a"))