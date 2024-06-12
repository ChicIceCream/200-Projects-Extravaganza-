def count_dots(string):
    dot_count = 0
    for char in string:
        if char == '.':
            dot_count += 1
    
    return dot_count

print(count_dots("h.a.h.a."))