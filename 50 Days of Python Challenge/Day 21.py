def make_tuples(list1, list2):
    
    if len(list1) != len(list2):
        return False
    
    final_list = list1 + list2
    
    return final_list

print(make_tuples([1,2,3,4], [5,6,7,8]))