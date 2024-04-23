def flat_list(nested_list):
    final_list = []
    for list in nested_list:
        final_list.extend(list)
    return final_list

print(flat_list([[2,4,5,6],[3,5,8,76]]))