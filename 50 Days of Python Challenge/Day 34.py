def just_digits():
    with open('50 Days of Python Challenge\Components\python.csv', 'r', encoding='utf-8') as file:
        a = file.read().split()
        
        result = []
        
        for word in a:
            if word.isdigit():
                result.append(word)
    return result
print(just_digits())