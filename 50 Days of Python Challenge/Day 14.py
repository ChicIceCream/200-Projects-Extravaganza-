def flat_list(nested_list):
    final_list = []
    for list in nested_list:
        final_list.expand(list)
    return final_list

print(flat_list([[2,4,5,6]]))