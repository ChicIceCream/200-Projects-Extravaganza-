from collections import defaultdict

def sort_words(string):
    
    hashmap = defaultdict(int)
    
    words = ''.join(string.split())
    
    for letter in words:
        hashmap[letter] += 1
    
    letters = []
    for x, count in hashmap.items():
        if count >= 1:
            letters.append(x)
    
    return sorted(letters)

print(sort_words('love life'))