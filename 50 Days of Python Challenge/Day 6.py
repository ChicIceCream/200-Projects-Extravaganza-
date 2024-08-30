def my_function(email):
    name = ""
    for letter in email:
        if letter != '@':
            name += letter
        else:
            break
    return name

email = "ben@gmail.com"
print(my_function(email))