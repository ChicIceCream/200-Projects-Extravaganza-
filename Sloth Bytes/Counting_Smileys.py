import re

def countSmileys(array):
    mapping = {
        ":)": True,
        ":-)": True,
        ":~)": True,
        ";)": True,
        ";-)": True,
        ";~)": True,
        ":D": True,
        ":-D": True,
        ":~D": True,
        ";D": True,
        ";-D": True,
        ";~D": True,
        ";-)": True,
    }
    count = 0
    
    if array == "":
        return 0
    for face in array:
        if face in mapping:
            count += 1
    return count

def countSmileys2(array):
    pattern = re.compile(r'^[:;][-~]?[)D]$')
    count = 0
    for face in array:
        if pattern.match(face):
            count += 1
    return count


print(countSmileys2([":)", ";(", ";}", ":-D"]))
output = 2 # the two smileys are [":)" and ":-D"

print(countSmileys2([";D", ":-(", ":-)", ";~)"]))
output = 3 #The three smileys are ";D", ":-)", and ";~)"

print(countSmileys2([";]", ":[", ";*", ":$", ";-D"]))
output = 1 #The smiley is ";-D"


print(countSmileys([":)", ";(", ";}", ":-D"]))
output = 2 # the two smileys are [":)" and ":-D"

print(countSmileys([";D", ":-(", ":-)", ";~)"]))
output = 3 #The three smileys are ";D", ":-)", and ";~)"

print(countSmileys([";]", ":[", ";*", ":$", ";-D"]))
output = 1 #The smiley is ";-D"