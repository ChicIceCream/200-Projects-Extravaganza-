def add_hash(string):
    words = string.split()
    
    hashed_string = "#".join(words)
    
    return hashed_string

def add_underscore(string):
    return string.replace('#','_')

def remove_underscore(string):
    return string.replace('_', ' ')

print(remove_underscore(add_underscore(add_hash('Python'))))