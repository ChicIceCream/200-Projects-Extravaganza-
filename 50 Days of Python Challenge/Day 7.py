# Code comment: (generated)
# **Test Case 1:**
# * Input: 0
# * Expected Output: ""
# 
# **Test Case 2:**
# * Input: 3
# * Expected Output: "0.1.2"
# 
# **Test Case 3:**
# * Input: 5
# * Expected Output: "0.1.2.3.4"
# 
# **Test Case 4:**
# * Input: 10
# * Expected Output: "0.1.2.3.4.5.6.7.8.9"
# 
# **Test Case 5:**
# * Input: -1
# * Expected Output: Index error
def string_range(number):
    string = []
    for i in range(number):
        string.append(str(i))
        string.append(".")
    
    if string[-1] == ".":
        string.pop()
    
    return ''.join(string)

integer = 3
print(string_range(integer))