a = []
u = int(input("Enter the number of elements present in the list : "))

for x in range(u):
    element = input(f"Enter element number {x + 1} :  ")
    a.append(element)

print(f"Element list : {a}")    

c = []
b = input("Enter the word to remove: ")

for i in a:
    if i != b:
        c.append(i)

print(f"Updated List : {c}")  