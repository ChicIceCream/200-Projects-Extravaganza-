"""

Write a function called divide_or_square that takes one argument (a
number), and returns the square root of the number if it is divisible by
5, returns its remainder if it is not divisible by 5.

"""

def divide_square(num):
    """Gives the root of number is divisible by 5, else gives its remainder"""
    
    if num % 5 == 0:
        # ** is used to check for root
        return f'{num ** 0.5:.2f}' # .2f specifies to give hte answer in 2 decimal places
    else:
        return f'{num % 5}'

# Get the input from the user, and remember to change it to an integer
number = int(input("Give me a number : "))
print(divide_square(number))