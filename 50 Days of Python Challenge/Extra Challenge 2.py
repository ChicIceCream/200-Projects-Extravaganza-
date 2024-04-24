def your_salary(name, rate, rate_overtime, periods):
    
    if periods > 100:
        salary = (100 * rate) + ((periods - 100) * rate_overtime)
    else:
        salary = (100 * periods)
    
    return f'Teacher : {name}'


teacher_name = input("What is the teachers name? : ")
salary = int(input(f"What is {teacher_name}'s salary? : "))
period_number = int(input("How many periods have they taught this month? : "))
rate = int(input(f"What is {teacher_name}'s rate for each period they take? : "))
rate_overtime = int(input(f"What is their rate for overtime? : "))