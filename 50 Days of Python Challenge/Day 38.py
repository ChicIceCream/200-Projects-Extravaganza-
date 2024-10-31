import random
import time 

def guess_a_number():
    number_to_guess = random.randint(0,10)
    
    print("Welcome to Number Guessing!")
    time.sleep(1)
    
    while True:
        number_guessed = int(input("Guess a number between 0 to 10 : "))
        if number_guessed > number_to_guess:
            print("Guess is too high! Try again!")
        elif number_guessed < number_to_guess:
            print("Guess is too low! Try Again!")
        else:
            return "Correct! Well Done!"

print(guess_a_number())