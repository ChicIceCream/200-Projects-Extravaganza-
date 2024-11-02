def translate(input_string):
    final = []
    vowels = ["a", "e", "i", "o", "u"]
    for word in list(input_string.split()):
        if word[0] in vowels:
            final.append(word + "yay")
            print(final)
        else:
            final.append(word[1:] + word[0] + "ay")
            print(final)
    return " ".join(final)

print(translate("i love python"))