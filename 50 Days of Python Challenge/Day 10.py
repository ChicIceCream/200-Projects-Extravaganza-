# def hide_password():
#     actual_password = input("Give me your password : ")
    
#     return f' Your password is : **** and it is 4 characters long'

# print(hide_password())

######################################################################### 

def bonus_challenge(list):
    new_list = []
    for number in list:
        string_number = str(number)
        new_list.append(number)

    return new_list

list = [1000000, 2356989, 2354672, 9878098]
print(bonus_challenge(list))
