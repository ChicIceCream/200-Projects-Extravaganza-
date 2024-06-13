def sum_list(num_list):
    final_list = []
    for num in num_list:
        for a in num:
            final_list.append(a)
    # total = 0
    
    # for num in final_list:
    #     total += num
    
    # return total
    return final_list

num_list = [[2, 4, 5, 6], [2, 3, 5, 6]]
print(sum_list(num_list))