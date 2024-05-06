from collections import defaultdict

def all_the_same(list):
    
    hashmap = defaultdict(int)
    
    for word in list:
        hashmap[word] += 1
    
    if len(hashmap.values()) > 1:
        return False

    return True

print(all_the_same(['Mary', 'Mary', 'Mary']))