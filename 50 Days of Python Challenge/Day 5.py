def my_discount():
    discount_price = price * (discount / 100)
    return price - discount_price

price = int(input("Give me the price : "))
discount = int(input("Give me the discount : "))
print(f' The final price is : {my_discount()}')
