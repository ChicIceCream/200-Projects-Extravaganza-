def tally_affirmative_responses(register):
    counter = 0
    for key in register:
        if register[key] == 'yes':
            counter += 1
    return counter + 

register = {
    'Michael':'yes','John': 'no',
    'Peter':'yes', 'Mary': 'yes'
            }
print(f'The amount of students present are : {register_check(register)}')