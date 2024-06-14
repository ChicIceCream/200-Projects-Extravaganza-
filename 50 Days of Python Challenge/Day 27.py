from collections import defaultdict


def unique_numbers(numbers):
    hashmap = defaultdict(int)
    
    for num in numbers:
        hashmap[num] += 1
    
    unique_list = []
    
    for num in hashmap:
        unique_list.append(num)
    
    # print(unique_list)
    # print(numbers)
    
    if (sum(numbers) - sum(unique_list)) % 2 == 0:
        print(f"the sum of unique is:  {sum(unique_list)} and their difference is {sum(numbers) - sum(unique_list)}")
        return numbers
    else:
        print(f"the sum of unique is:  {sum(unique_list)} and their difference is {sum(numbers) - sum(unique_list)}")
        return unique_list

print(unique_numbers([1, 2, 4, 5, 6, 7, 8, 8]))
