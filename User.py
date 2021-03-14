import datetime
import re
import uuid

import Console
from Database import Database as db
from MenuDependency import show_user_menu
from Product import Product
from Validator import is_valid_price, is_valid_product_category, is_valid_product_name
from Validator import is_valid_user_name, is_valid_password, is_valid_email, is_valid_quantity, valid_passwords


class User:
    def __init__(self, first_name, last_name, user_name, email, password, date_joined):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_name = user_name
        self.password = password
        self.date_joined = date_joined

    def change_password(self):
        print('----Change Password----')
        print('To go back enter "/back"\n')

        attempts_left = 5
        current_password = input('Enter current password: ')
        if current_password == '/back':
            self.show_dashboard()

        while current_password != self.password:

            if attempts_left < 1:
                self.logout()
            elif attempts_left < 2:
                incorrect_message = f'\nIncorrect password. You will be logged out after one more incorrect attempt.'
            else:
                incorrect_message = f'\nIncorrect password. Try again ({attempts_left} attempts left.)'

            print(incorrect_message, '\n')
            attempts_left -= 1
            current_password = input('Enter current password: ')
            if current_password == '/back':
                Console.clear_screen(1)
                self.show_dashboard()

        new_password = input('Enter new password: ')
        while not is_valid_password(new_password):
            new_password = input('Enter new password: ')

        confirm_password = input('Confirm password: ')
        while not valid_passwords(new_password, confirm_password):
            new_password = input('Enter new password: ')
            while not is_valid_password(new_password):
                new_password = input('Enter new password: ')

            confirm_password = input('Confirm password: ')

        self.password = new_password
        db.update_user_password(self)
        print('Password changed.')
        Console.clear_screen(3)
        self.show_dashboard()

    def change_email(self):
        print('----Change Email----')
        print('To go back enter "/back"\n')
        print(f'Current Email: {self.email}\n')
        new_email = input('Enter new email address: ')
        if new_email == '/back':
            Console.clear_screen(1)
            self.show_dashboard()

        while not is_valid_email(new_email):
            new_email = input('Enter new email address: ')

        password = input('Enter password to confirm change: ')
        while password != self.password:
            password = input('Enter password to confirm change: ')

        self.email = new_email
        db.update_user_email(self)

        print('\nEmail changed.')
        Console.clear_screen(3)
        self.show_dashboard()

    def change_user_name(self):
        print('----Change User Name----')
        print('To go back enter "/back"\n')
        print(f'Current User Name: {self.user_name}\n')
        new_user_name = input('Enter new user name: ')
        if new_user_name == '/back':
            Console.clear_screen(1)
            self.show_dashboard()

        while not is_valid_user_name(new_user_name):
            new_user_name = input('Enter new user name: ')

        password = input('Enter password to confirm change: ')
        while password != self.password:
            print('\nWrong password!\n')
            password = input('Enter password to confirm change: ')

        self.user_name = new_user_name
        db.update_user_user_name(self)

        print('\nUser Name changed.')
        Console.clear_screen(3)
        self.show_dashboard()

    def restock(self):
        print('----Restock a Product----\n')
        print('1. Select product from list\n2. Select product by name\n3. Back\n')
        action = input('--> ')
        while not re.match(r'^[1-3]$', action):
            print('\nInvalid input. Try again\n')
            action = input('--> ')

        if action == '1':
            Console.clear_screen(0)
            product_list = self.product_list('Select a product to restock. To go back enter "/back"', True)
            if len(product_list) > 0:
                while True:
                    action = input("--> ")
                    if action == '/back':
                        Console.clear_screen(1)
                        show_user_menu(self)
                    elif re.match(r'^\d+$', action):
                        while int(action) > len(product_list):
                            print('No product found at selected index.')
                            action = input("--> ")

                        selected_index = int(action)
                        selected_product = product_list[selected_index - 1]
                        print(f'Restock {selected_product.name}\n')
                        quantity = input('Quantity: ')
                        while not is_valid_quantity(quantity):
                            quantity = input('Quantity: ')
                        selected_product.quantity = str(int(selected_product.quantity) + int(quantity))
                        db.restock_product(selected_product)
                        print(f'{selected_product.name} Restocked\nAdded {quantity} pieces')
                        Console.clear_screen(3)
                        self.restock()

                    else:
                        print("\nError: Invalid input")
            else:
                print('You currently have no products.\n')
                while input("--> ") != '/back':
                    input('-->')

                Console.clear_screen(0)
                show_user_menu(self)

        elif action == '2':
            product_list = self.product_list('Restock product by name. To go back enter "/back"\n', False)
            product_name = input('Enter Product name: ')
            found = False
            for i in range(len(product_list)):
                if product_list[i].name == product_name:
                    product_to_restock = product_list[i]
                    quantity = input('Quantity: ')
                    while not is_valid_quantity(quantity):
                        quantity = input('Quantity: ')

                    product_to_restock.quantity = str(int(product_to_restock.quantity) + int(quantity))
                    db.restock_product(product_to_restock)
                    print(f'{product_to_restock.name} Restocked\nAdded {quantity} pieces')
                    found = True
                    break

            if not found:
                print(f'Product with the name {product_name} not found.')
                
            Console.clear_screen(2)
            self.restock()

        elif action == '3':
            Console.clear_screen(1)
            show_user_menu(self)

    def show_dashboard(self):
        print('----Account Details----\n')
        print(f'User ID: {self.id}')
        print(f'First Name: {self.first_name}')
        print(f'Last Name: {self.last_name}')
        print(f'User Name: {self.user_name}')
        print(f'Email: {self.email}')
        print('Password: ', '*' * len(self.password))
        print(f'Date Joined: {self.date_joined}')

        print('\n1. Change User Name\n2. Change Password\n3. Change Email\n4. Delete Account\n5. Back\n')
        action = input('--> ')
        while not re.match(r'^[1-6]$', action):
            print('Invalid input. Try again')
            action = input("--> ")

        if action == '1':
            Console.clear_screen(1)
            self.change_user_name()
        elif action == '2':
            Console.clear_screen(1)
            self.change_password()
        elif action == '3':
            Console.clear_screen(1)
            self.change_email()
        elif action == '4':
            Console.clear_screen(1)
            self.delete_account()
        elif action == '5':
            Console.clear_screen(1)
            show_user_menu(self)

    def add_new_product(self):
        print("----Add Product----\n")
        products = []
        add_more = True

        while add_more:
            owner_id = self.id
            product_name = input("Product Name: ")
            while not is_valid_product_name(product_name):
                product_name = input("Product Name: ")

            product_category = input("Product Category: ")
            while not is_valid_product_category(product_category):
                product_category = input("Product Category: ")

            product_price = input("Product Price: $")
            while not is_valid_price(product_price):
                product_price = input("Product Price: $")

            product_quantity = input('Product Quantity: ')
            while not is_valid_quantity(product_quantity):
                product_quantity = input('Product Quantity: ')

            now = datetime.datetime.now()
            date_added = now.strftime("%d-%m-%Y")
            product = Product(owner_id, product_name, product_category, product_price, product_quantity, date_added)
            products.append(product)
            response = input("\nAdd another product (Y/N): ").lower()
            if response == 'n':
                add_more = False

        db.insert_products(products)
        if len(products) > 1:
            print('Products have been added.\n')
        else:
            print('Product has been added.\n')
        Console.clear_screen(2)
        show_user_menu(self)

    def delete_product(self):
        print('----Delete Product----\n')
        print('1. Delete product from list\n2. Delete product by name\n3. Back\n')

        action = input('--> ')
        while not re.match(r'^[1-3]$', action):
            print('\nInvalid input. Try again\n')
            action = input('--> ')

        if action == '1':
            Console.clear_screen(1)
            product_list = self.product_list('Select a product to delete. To go back enter "/back"', True)
            if len(product_list) < 1:
                print("You currently don't have any products.\n")
                action = input("--> ")
                while action != '/back':
                    action = input("--> ")
                    print("\nError: Invalid input")

                Console.clear_screen(0)
                self.delete_product()
            else:
                selected_index = input('--> ')
                while int(selected_index) > len(product_list):
                    print('\nNo product found at selected index\n')
                    selected_index = input('--> ')
                product_to_delete = product_list[int(selected_index) - 1]
                print(f'\nDelete {product_to_delete.name}\nAre you sure you want to delete this product?(Y/N)')
                choice = input('--> ').lower()
                while choice != 'n' and choice != 'y':
                    print('\nInvalid input.\n')
                    choice = input('--> ').lower()

                if choice == 'y':
                    db.delete_product(product_to_delete)
                    print('Deleted successfully.')
                    Console.clear_screen(2)
                    self.delete_product()
                else:
                    Console.clear_screen(1)
                    self.delete_product()

        elif action == '2':
            Console.clear_screen(1)
            product_list = self.product_list('Delete product by name. To go back enter "/back"', False)
            product_name = input('Enter product name: ')

            found = False
            for i in range(len(product_list)):
                if product_list[i].name == product_name:
                    product_to_delete = product_list[i]
                    db.delete_product(product_to_delete)
                    found = True
                    break

            if not found:
                print(f'Product with the name {product_name} not found.')
                Console.clear_screen(1)
                self.delete_product()

        else:
            Console.clear_screen(1)
            show_user_menu(self)

    def view_products(self):
        product_list = self.product_list('Select a product to view details. To go back enter "/back"', True)
        if len(product_list) < 1:
            print("You currently don't have any products.\n")
            action = input("--> ")
            while action != '/back':
                print("\nError: Invalid input\n")
                action = input("--> ")

            Console.clear_screen(0)
            show_user_menu(self)

        while True:
            action = input("--> ")
            if action == '/back':
                Console.clear_screen(0)
                show_user_menu(self)
            elif re.match(r'^\d+$', action):
                selected_index = int(action)
                selected_product = product_list[selected_index - 1]
                Console.clear_screen(1)
                self.view_product_detail(selected_product)
            else:
                print("\nError: Invalid input")

    def product_list(self, message, show_list):
        print("----Product List----")
        print(message)
        product_tuple = db.get_all_product(self.id)
        product_list = []

        index = 1
        for i in product_tuple:
            product = Product(i[1], i[2], i[3], i[4], i[5], i[6])
            product.product_id = i[0]
            product_list.append(product)

        if show_list:
            for product in product_list:
                print(f'{index}. {product.name}')
                index += 1
            print()
        return product_list

    def view_product_detail(self, product):
        print("----Product Details----\n")
        print(f'Product ID: {product.product_id}')
        print(f'Owner ID: {product.owner_id}')
        print(f'Product Name: {product.name}')
        print(f'Product Category: {product.category}')
        print(f'Product Price: ${product.price}')
        print(f'Product Quantity: {product.quantity}')
        print(f'Product Date Added: {product.date_added}')
        action = input('\nTo go back enter "/back": ').lower()
        while action != '/back':
            action = input('To go back enter "/back": ').lower()
        Console.clear_screen(0)
        self.view_products()

    def logout(self):
        from App import show_main_menu
        show_main_menu()

    def delete_account(self):
        print('----Delete Account----')
        print('To go back enter "/back"\n')
        print(f'User ID: {self.id}\nEnter User ID above to delete this account.')
        action = input('--> ')

        while action != self.id and action != '/back':
            print('\nInvalid input\n')
            action = input('--> ')

        if action == self.id:
            db.delete_user(self)
            print('Account deleted!')
            Console.clear_screen(5)

        elif action == '/back':
            show_user_menu(self)
