def convert_add(str_list):
    # This will convert every number that is a string to an integer
    int_list = [int(num) for num in str_list]
    
    # Another way to do this is using the map() function
    # int_list =  list(map(int, list))
    
    total = 0  # Initialize total outside of the loop
    
    for i in int_list:
        total += i  # Use the += operator to increment total
    
    # Another very easy way to get the total is to use the sum() function
    # total = sum(int_list)
    
    return total

string_list = ['1', '3', '5']
print(convert_add(string_list))