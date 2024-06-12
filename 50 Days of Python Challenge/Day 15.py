def same_in_reverse(string):
    reversed_str = string[::-1]
    
    # print(reversed_str, string)
    
    return reversed_str == string

print(same_in_reverse("dad"))