def count_letters(nef):
    nef = nef.replace(" ","")
    return f'The string has {len(nef)}'

print(count_letters(" I am a Idiot")