def my_discount():
    price = int(input("Give me the price : "))
    discount = int(input("Give me the discount : "))
    discount_price = price * (discount / 100)
    return price - discount_price

print(f' The final price is : {my_discount()}')