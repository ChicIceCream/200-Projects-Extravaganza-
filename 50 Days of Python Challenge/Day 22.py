def add_hash(string):
    words = string.split()
    
    hashed_string = "#".join(words)
    
    return hashed_string

print(add_hash("hello everyone"))