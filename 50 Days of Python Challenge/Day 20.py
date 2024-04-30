def capitalize(string):
    new_string = string.split()
    list(new_string)
    
    for i in range(len(new_string)):
        new_string[i] = new_string[i][0].upper() + new_string[i][1:]
        
    capitalized_string = ' '.join(new_string)
    
    return capitalized_string

print(capitalize("Today is good day"))