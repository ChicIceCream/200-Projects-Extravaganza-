from collections import defaultdict

def repeated_name(list_of_names):
    hashmap = defaultdict(int)
    
    for name in list_of_names:
        hashmap[name] += 1
    
    most_repeated_name = max(hashmap, key=hashmap.get)
    
    return most_repeated_name

print(repeated_name(["John", "Peter", "John", "Peter", "Jones", "Peter"]))