def your_vat():
    while True:
        try:
            value = int(input("Give me the price : "))
            try:
                VAT = int(input("Give me the VAT as a percentage : "))
                break
            except ValueError:
                print("Give me a valid number : ")
        except ValueError:
            print("Give me a valid number : ")
    
    return 1

print(your_vat())

