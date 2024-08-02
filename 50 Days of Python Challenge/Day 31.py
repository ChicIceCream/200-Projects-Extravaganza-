from collections import defaultdict


def longest_word(array):
    
    hashmap = defaultdict(int)
    for word in array:
        hashmap[word] = len(word)
    
    longest = max(hashmap, key=hashmap.get)
    
    return hashmap[longest], longest


print(longest_word(['Java', 'JavaScript', 'Python']))