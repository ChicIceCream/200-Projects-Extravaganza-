def inter_section(list1, list2):
    result = []
    for num in list1:
        for number in list2:
            if num == number:
                result.append(num)
    
    return tuple(result)

def inter_section(a, b):
    return tuple(i for i in a if i in b)

print(inter_section([20, 30, 60, 65, 75, 80, 85], [42, 30, 80, 65, 68, 88, 95]))