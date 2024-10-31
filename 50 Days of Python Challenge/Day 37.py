from collections import defaultdict

def count_the_vowels(input_string):
    counter = defaultdict(int) # make a defaultdict for counter
    vowels = ["a", "e", "i", "o", "u"] # make a list to check if the characters is one of thw vowel
    
    for char in input_string.lower(): # to make sure it only counts the vowel once 
        if char in vowels:    # only include the character if it is a vowel
            counter[char] += 1
    
    return len(counter.keys())    # will return the length of the keys

print(count_the_vowels("hello"))