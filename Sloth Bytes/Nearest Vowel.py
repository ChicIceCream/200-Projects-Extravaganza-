def nearest_vowel(letter):
    num = ord(letter)
    vowels = ['a', 'e', 'i', 'o', 'u']
    
    closest_vowel = vowels[0]
    min_diff = abs(num - ord(closest_vowel))
    
    for vowel in vowels[1:]:
        diff = abs(num - ord(vowel))
        if diff < min_diff:
            min_diff = diff
            closest_vowel = vowel
    
    return closest_vowel

print(nearest_vowel("b")) 
output = "a" # closest vowel is a
print(nearest_vowel("s")) 
output = "u" # closest vowel is u
print(nearest_vowel("c"))
output = "a" # closest vowel is a
print(nearest_vowel("i"))
output = "i" # i is a vowel, so return itself
print(nearest_vowel("z"))
output = "u" # to make sure there is no wrapping