# Code review: (generated)
# Use `sum(1 for key in register if register[key] == 'yes')` for conciseness and efficiency.  This avoids explicit loop and counter.
# 
def count_yes_in_register(register):
    counter = 0
    for key in register:
        if register[key] == 'yes':
            counter += 1






























# register = {
#     'Michael':'yes','John': 'no',
#     'Peter':'yes', 'Mary': 'yes'
#             }
# print(f'The amount of students present are : {register_check(register)}')