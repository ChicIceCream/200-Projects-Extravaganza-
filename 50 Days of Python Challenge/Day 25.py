from collections import defaultdict

def all_the_same(list):
    
    hashmap = defaultdict(int)
    
    for word in list:
        hashmap[word] += 1
    
    if len(hashmap.values()) > 1:
        return False

    return len(list) == len(hashmap.values())

print(all_the_same(['Mary', 'Mary', 'Mary']))

# def all_the_same(data:str or list or tuple):
#     neel2 = defaultdict(int)
#     for word in data:
#         neel2[word] += 1
#     if len(data) == neel2.values():
#         print("values are same")
#     return neel2
# print(all_the_same(['Mary', 'Mary' ,'Mary']))