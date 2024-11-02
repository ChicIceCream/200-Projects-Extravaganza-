def words_with_vowels(input_string):
    final = []
    vowels = ["a", "e", "i", "o", "u"] # make a vowel lsit to check if it exists in the word
    
    for word in list(input_string.split()): # list so we can iterate over every word
        for letter in word:
            if letter in vowels: # double for loop to check in letters
                final.append(word)
                break # break so it doesnt repeat for every vowel in the word 
    
    return final

print(words_with_vowels("You have no rhythm"))