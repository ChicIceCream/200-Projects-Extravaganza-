from collections import defaultdict

def check_pangram(input_string):
    counter = defaultdict(int) # Make a dictionary that counts 
    stripped_string = "".join(input_string.split()) # To remove all the white spaces
    
    for char in stripped_string.lower(): # Make it all lowercase so it takes in capital and lower as same character
        counter[char] += 1
    
    # If the number of keys are 26 then that means there are 26 alphabets
    if len(counter.keys()) == 26:
        # print(counter.keys()) # checking 
        return True
    else:
        # print(len(counter.keys())) # checking
        return False

print(check_pangram("the quick brown fox jumps over a lazy dog"))