def words_with_vowels(input_string):
    final = []
    vowels = ["a", "e", "i", "o", "u"]
    
    for word in list(input_string.split()):
        for letter in word:
            if letter in vowels:
                final.append(word)
                break
    
    return final

print(words_with_vowels("You have no rhythm"))