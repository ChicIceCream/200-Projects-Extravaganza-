def translate(input_string):
    final = []
    vowels = ["a", "e", "i", "o", "u"] # added vowels to check if the word has vowels in it
    
    for word in list(input_string.split()): # split so every word is individual and list so we can iterate over the word
        if word[0] in vowels: # if the first letter has a vowel
            final.append(word + "yay")
        else: # if it doesnt
            # iterates over the whole word after the first letter, adds the first letter and adds "ay" at the end
            final.append(word[1:] + word[0] + "ay") 
            
    return " ".join(final) # join because the whole final variable is a list, not a sentence

print(translate("i love python"))