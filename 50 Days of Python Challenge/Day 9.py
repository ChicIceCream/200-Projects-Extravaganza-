def biggest_odd(list):
    new_list = [letter for letter in list if int(letter) % 2 != 0]
    
    return max(new_list)

list = "23569"
print(biggest_odd(list))