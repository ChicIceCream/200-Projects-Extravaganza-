from collections import defaultdict

def longest_word(array):
    
    hashmap = defaultdict(int)
    for word in array:
        hashmap[word] = len(word)
    
    longest = max(hashmap, key=hashmap.get)
    
    return hashmap[longest], longest

print(longest_word(['Java', 'JavaScript', 'Python']))

# Another method

def longest_word(array):
    if not array:  # Check if the array is empty
        return ""
    
    longest = array[0]
    
    for word in array:
        if len(word) > len(longest):
            longest = word
    
    return longest, len(longest)

print(longest_word(['Java', 'JavaScript', 'Python']))


