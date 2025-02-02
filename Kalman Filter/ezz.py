stars = input("how many fucking stars do you want? : ")
for i in range(int(stars), 0, -1):
    print(" " * (int(stars) - i) + "*" * i)
