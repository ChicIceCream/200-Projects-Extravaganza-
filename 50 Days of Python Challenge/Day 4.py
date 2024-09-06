def only_floats(a, b):
    count = 0
    if type(a) == float:
        count += 1
    
    if type(b) == float:
        count += 1
    
    return count
