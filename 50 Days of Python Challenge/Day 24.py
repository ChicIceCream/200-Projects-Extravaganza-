def average_calories():
    calories_total = int(input("Enter the anount of total calories you have taken?: "))
    days = int(input("How many days were total?:  "))
    
    return f'The amount of average calories taken is : {int(calories_total / days)}'

print(average_calories())