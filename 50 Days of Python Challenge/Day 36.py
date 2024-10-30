from collections import defaultdict

def count(input_string):
    counter = defaultdict(int) # Create a simple dictionary
    
    for char in input_string:
        counter[char] += 1
        
    return counter.items() # Items returns both key and value pairs

print(count("hello"))

def count(a):
    dictionary = {}
    for i in range(len(a)):
        x = a[i]
        count = 0
        for j in range(i, len(a)):
            if a[j] == a[i]:
                count = count + 1
        countz = dict({x: count})
        # updating the dictionary
        if x not in dictionary.keys():
            dictionary.update(countz)
    return dictionary
print(count('hello'))