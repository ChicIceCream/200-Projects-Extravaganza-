def any_number(*args):
    total = 0
    num_of_args = 0
    for arg in args:
        total += arg
        num_of_args += 1
    
    return total / num_of_args

print(any_number(12,90))
'''
I learned something new today! it is about the "*args". 
I found out that we can input any number of inputs and 
they are stored as a tuple!
'''