def odd_even(list):
    left, right = 0, len(list) - 1
    # print(left, right)
    while left != right:
        if list[right] % 2 != 0:
            right -= 1
            # print(right)
        if list[left] % 2 != 1:
            left += 1
            # print(left)
        
        # print(f'{list[left]} and {list[right]}')
        return list[right] - list[left]


# print(odd_even(list))
# print(f'{6 % 2}')
# your_list = [1,4,5,6,7]
my_list = [1,2,3,4,6]

def odd_even2(list):
    for num in list:
        if num % 2 == 0:
            even = num
    
    for num in list:
        if num % 2 != 0:
            odd = num
            break
        
    return even, odd

print(odd_even2(my_list))