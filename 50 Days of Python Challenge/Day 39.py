import random
import string

def generate_password():
    password = []
    password_security = input('''Choose Your Security Level :
            1 -> Low Security 
            2 -> Strong Security
            3 -> Very Strong Security
    :''')
    
    if password_security == "1":
        length = 5
    elif password_security == "2":
        length = 8
    elif password_security == "3":
        length = 12
    else:
        print("Wrong Input. Please try again!")
    
    for i in range(length):
        password.append(random.choice(string.ascii_letters + string.digits + string.punctuation))
    
    return ''.join(password)

print(generate_password())