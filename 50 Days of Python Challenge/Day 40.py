def translate(input_string):
    final = []
    vowels = ["a", "e", "i", "o", "u"]
    for word in list(input_string):
        if word[0] in vowels:
            final.append(word + "yay")

