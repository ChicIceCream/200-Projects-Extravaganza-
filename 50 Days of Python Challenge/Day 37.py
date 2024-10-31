from collections import defaultdict

def count_the_vowels(input_string):
    counter = defaultdict(int)
    vowels = ["a", "e", "i", "o", "u"]
    
    for char in input_string:
        if char in vowels:    
            counter[char] += 1
    
    return len(counter.keys())    

print(count_the_vowels("hello"))