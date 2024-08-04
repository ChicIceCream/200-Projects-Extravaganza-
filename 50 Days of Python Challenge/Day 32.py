def password_validator():
    password = input("Enter your password: ")
    
    while True:
        if len(password) < 8: # longer than 8 letters
            print("Password should be atleast 8 letters long")
        elif not any(c.isupper() for c in password): # upper case letter
            print("Password should contain at least one uppercase letter")
        elif not any(c.islower() for c in password): # lower case letter
            print("Password should contain at least one lowercase letter")
        elif not any(c.isdigit() for c in password): # atleast on digit
            print("Password should contain at least one digit")

