def index_position(string):
    index = []
    
    for letter in string:
        if letter.lower() == letter:
            index.append(letter.index())
    
    return index

print(index_position("LovE"))