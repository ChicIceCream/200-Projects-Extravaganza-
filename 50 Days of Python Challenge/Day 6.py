def user_name(email):
    name = ""
    for letter in email:
        if letter != '@':
            name += letter
        else:
            break
    return name

email = "ben@gmail.com"
print(user_name(email))