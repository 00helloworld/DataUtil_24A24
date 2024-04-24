# File: Project3.py
# Student: 
# UT EID: Writer Contact Personal: d497465762@gmail.com
# Course Name: CS303E
# 
# Date Created: April 23, 2024
# Description of Program: 

import os

class Product:
    def __init__(self, sku: int, company: str, description: str, price: float):
        self.__sku = sku
        self.__company = company
        self.__description = description
        self.__price = price

    def get_sku(self) -> int:
        return self.__sku

    def get_company(self) -> str:
        return self.__company

    def get_description(self) -> str:
        return self.__description

    def get_price(self) -> float:
        return self.__price
    
    def __str__(self) -> str:
        return f'    {self.__sku}:  ${self.__price} {self.__company} {self.__description}'


def init_database(file):
    with open(file) as f:
        lines = f.readlines()

    database = {}
    sku = 1
    for l in lines:
        if l[0] == '#':
            continue
        company = l.split(',')[0]
        description = l.split(',')[1]
        price = round(float(l.split(',')[2]), 2)
        product = Product(sku, company, description, price)
        database[sku] = product
        sku += 1

    return database

def help_():
    output = '''
The following commands are available:
    Help     - show available commands;
    Exit     - exit the application, without purchasing anything;
    Brands   - list the brands/companies available;
    Search   - display products matching the brand and/or description keywords;
    Add      - add a product to your shopping cart by Sku number;
    Remove   - remove a product from your shopping cart by Sku number;
    Cart     - display the current contents of your shopping cart;
    Checkout - display a customer "receipt" from purchasing the contents of the shopping cart.
    '''
    print(output)


def exit_():
    output = '''
    Thanks for shopping with us! Please come back soon.
    '''
    print(output)


def brands_(data):
    brands = []
    for k,v in data.items():
        brand = v.get_company()
        if brand not in brands:
            brands.append(brand)
            
    output = "\nWe have cheeses available from all of the following brands:\n    "
    # output += ", ".join(brands[:-1]) + ", and " + brands[-1] + "."

    formatted_brands = [", ".join(brands[i:i + 5]) for i in range(0, len(brands), 5)]
    output += "\n    ".join(formatted_brands) + "."
    print(output)


def contains_all_keywords(target_str, keywords):
    for keyword in keywords:
        if keyword.lower() not in target_str.lower():
            return False
    return True


def search_(data):
    brand = None
    keywords = None
    print()
    brand_ = input('    Brand (or return for any brand):')
    keywords_ = input('    Product keywords (or return for any):')
    if brand_ != '':
        brand = brand_
    if keywords_ != '':
        keywords = keywords_.split(' ')

    if brand is None:
        filter_brand = [v for k, v in data.items()]
    else:
        filter_brand = [v for k, v in data.items() if brand in v.get_company().lower()]

    if keywords is None:
        filter_kw = filter_brand
    else:
        filter_kw = [i for i in filter_brand if contains_all_keywords(i.get_description(), keywords)]

    if len(filter_kw) > 0:
        print('\nFound the following matching products:')
        for product in filter_kw:
            print(product)
    else:
        print('\nNo matching products found.')


def add_(data, cart):
    print()
    sku = input('    Enter product Sku to add to cart:')
    try:
        sku = int(sku)
    except:
        print('Sku should be integer!')
        return cart
    
    if sku in data:
        cart.append(data[sku])
    else:
        print(f'No product with Sku {sku} found.')

    return cart


def remove_(cart):
    print()
    sku = input('    Enter product Sku to remove from cart:')
    try:
        sku = int(sku)
    except:
        print('sku should be integer!')
        return cart
    
    flag = 0
    if len(cart) > 0:
        for i in cart:
            if i.get_sku() == sku:
                cart.remove(i)
                flag = 1
                break
        if flag == 0:
            print(f'No product with Sku {sku} found.')
    else:
        print(f'No product with Sku {sku} found.')

    return cart


def cart_(cart):
    print('\nYour shopping cart contains:')
    price = 0
    for i in cart:
        print(i)
        price += i.get_price()
    print(f'Cart contains {len(cart)} items, for a total cost of ${price:.2f}')


def checkout_(cart):
    print('\nYou have purchased the following items:')
    price = 0
    for i in cart:
        print(i)
        price += i.get_price()
    print(f'Summary: {len(cart)} items for a total cost of ${price:.2f}')
    print('\nThanks for shopping with us! Please come back soon.')




def main():
    file_name = input('Enter data filename:').strip()
    if file_name == '':
        file_name = 'Cheeses.csv'
    if not os.path.exists(file_name):
        print(f'Cannot find file: {file_name}')
        return
    
    print(f'Creating product database from file: {file_name}')
    database = init_database(file_name)
    print('\nWelcome to the online shopping app. We have a large selection of cheeses available from many popular brands. Happy shopping!')
    cart = []

    while True:
        print()
        command = input('Enter a command (help, exit, brands, search, add, remove, cart, checkout):').strip().lower()
        if command == 'exit':
            exit_()
            return
        elif command == 'help':
            help_()
        elif command == 'brands':
            brands_(database)
        elif command == 'search':
            search_(database)
        elif command == 'add':
            add_(database, cart)
        elif command == 'remove':
            remove_(cart)
        elif command == 'cart':
            cart_(cart)
        elif command == 'checkout':
            checkout_(cart)
            return
        else:
            print(f"\nSorry, your command wasn't recognized. Try again.")


        

if __name__ == '__main__':
    main()
        