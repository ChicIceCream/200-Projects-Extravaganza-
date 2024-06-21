def middle_figure(a, b):
    combined_string = a + b
    middle_index = len(combined_string) // 2
    middle_character = combined_string[middle_index]
    
    return middle_character

print(middle_figure("make love", "not war"))