def sum_list(num_list):
    final_list = []
    for num in num_list:
        final_list.extend(num)
    
    total = 0
    
    for num in final_list:
        total += num
    
    return total

num_list = [[2, 4, 5, 6], [2, 3, 5, 6]]
print(sum_list(num_list))