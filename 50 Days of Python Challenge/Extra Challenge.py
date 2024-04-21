def age_in_minutes():
    while True:
        try:
            year = int(input("Give me your birth year : "))
            if len(str(year)) == 4 and year >= 1900 and year < 2024:
                break
            else:
                print("Please enter a valid year")
        except:
            print("Please give me a value of 4 numbers")
    
    years_old_now = 2024 - year
    minutes = years_old_now * 12 * 30 * 24 * 60
    
    return f'You are around {minutes} minutes old right now!'

print(age_in_minutes())

