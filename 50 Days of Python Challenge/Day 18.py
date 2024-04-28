def any_number(*args):
    total = 0
    num_of_args = 0
    for arg in args:
        total += arg
        num_of_args += 1
    
    return total / num_of_args

print(any_number(12,90))