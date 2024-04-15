def string_range(number):
    string = []
    for i in range(number):
        string.append(str(i))
        string.append(".")

    if string[-1] == ".":
        string.pop()

    return ''.join(string)

integer = 9
print(string_range(integer))