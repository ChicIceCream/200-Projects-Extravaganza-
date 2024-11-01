import random
import string

def generate_password():
    password = [] # make an empty list to store the password at the end
    while True: # loops forever until the right answer is given
        password_security = input('''Choose Your Security Level :
                1 -> Low Security 
                2 -> Strong Security
                3 -> Very Strong Security
        :''')
        
        if password_security == "1":
            length = 5
            break
        elif password_security == "2":
            length = 8
            break
        elif password_security == "3":
            length = 12
            break
        else:
            print("Wrong Input. Please try again!")
    
    for i in range(length):
        # use random and string modules to make sure a random letter, digit or punctuation is chosen
        password.append(random.choice(string.ascii_letters + string.digits + string.punctuation)) 
    
    return f"Here is your generated password : {''.join(password)}"

print(generate_password())