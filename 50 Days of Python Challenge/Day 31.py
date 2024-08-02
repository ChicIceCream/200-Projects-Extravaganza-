from collections import defaultdict


def longest_word(array):
    return numberOfLetters(max(array))

def numberOfLetters(array):
    hashmap = defaultdict(int)
    for word in array:
        for letter in word:
            hashmap[word] += 1
    
    return hashmap.values()

print(longest_word(['Java', 'JavaScript', 'Python']))