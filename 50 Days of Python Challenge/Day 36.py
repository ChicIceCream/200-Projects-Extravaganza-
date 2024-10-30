from collections import defaultdict

def count(input_string):
    counter = defaultdict(int)
    
    for char in input_string:
        counter[char] += 1
        
    return counter.items()

print(count("hello"))