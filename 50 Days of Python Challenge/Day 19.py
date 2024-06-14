def count_words(string):
    words = string.split()
    
    return len(words)

def trial(string):
    words = string.replace(" ", ",")
    return words

def count_elements(string):
    words = string.split()
    
    characters = 0
    for letters in words:
        characters += len(letters)
    
    return characters

sentence = f"I love learning"
# print(f"Number of words: {count_words(sentence)}")  # Output: 3
# print(f"Number of elements: {count_elements(sentence)}")  # Output: 13\
print(trial("sentence"))