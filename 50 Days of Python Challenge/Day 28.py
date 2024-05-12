def index_position(string):
    index = []
    
    for i, letter in enumerate(string):
        if letter.lower() == letter:
            index.append(i)
    
    return index

print(index_position("LovE"))