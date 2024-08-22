def your_salary():
    
    teacher_name = input("What is the teachers name? : ")
    periods = int(input("How many periods have they taught this month? : "))
    rate = int(input(f"What is {teacher_name}'s rate for each period they take? : "))
    rate_overtime = int(input(f"What is their rate for overtime? : "))
        
    if periods > 100:
        salary = (100 * rate) + ((periods - 100) * rate_overtime)
    else:
        salary = (100 * periods)
    
    salary = "{:,.2f}".format(salary)
    
    return f'Teacher : {name} \nPeriods : {periods} \nGross Salary : {salary}'


print(your_salary())