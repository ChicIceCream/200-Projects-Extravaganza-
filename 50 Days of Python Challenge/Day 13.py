def your_vat():
    '''
    This function will convert our price and VAT into the final price
    and will also check if the inout is correct
    '''
    while True:
        # We will use a try and except case to make sure the right value is input
        try:
            value = int(input("Give me the price : "))
            try:
                VAT = int(input("Give me the VAT as a percentage : "))
                break
            except ValueError: # We use a ValueError to make sure the value entered is an integer
                print("Give me a valid number : ")
        except ValueError:
            print("Give me a valid number : ")
    
    return f'The total price is : ${int(value + (value * (VAT/100)))}' # Calculates the end answer

print(your_vat())

