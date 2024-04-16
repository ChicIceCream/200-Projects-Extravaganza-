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

list = [1,2,4,6]
print(odd_even(list))
# print(f'{6 % 2}')