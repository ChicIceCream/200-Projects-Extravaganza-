import random

def user_name():
    username = input("Please input your username : ")
    reversed_username = username[::-1]

    return (reversed_username + str(random.randint(0, 9)))

print(user_name())
