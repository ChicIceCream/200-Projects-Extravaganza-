def hide_password():
    actual_password = input("Give me your password : ")
    
    return f' Your password is : {"*" * (len(actual_password) - 1)} and it is {(len(actual_password) - 1)} characters long'

print(hide_password())
