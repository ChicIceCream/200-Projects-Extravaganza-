def equal_strings(str1, str2):
    if len(str1) != len(str2): 
        return False

    return sorted(str1) == sorted(str2)


str1 = 'haha'
str2 = 'haha'
print(equal_strings(str1, str2))