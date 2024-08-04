def password_validator():
    while True:
        password = input("Enter your password: ")
        
        if len(password) < 8:  # longer than 8 letters
            print("Password should be at least 8 letters long")
        elif not any(c.isupper() for c in password):  # upper case letter
            print("Password should contain at least one uppercase letter")
        elif not any(c.islower() for c in password):  # lower case letter
            print("Password should contain at least one lowercase letter")
        elif not any(c.isdigit() for c in password):  # at least one digit
            print("Password should contain at least one digit")
        else:
            print("Password is valid")
            break

password_validator()
