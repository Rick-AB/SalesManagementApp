import datetime
import re
import uuid

import Console
from Database import Database as db
from MenuDependency import show_admin_menu
from User import User
from Validator import is_valid_user_name, is_valid_password, is_valid_email, valid_passwords, \
    is_valid_name, format_name


class Admin:
    def __init__(self, first_name, last_name, user_name, email, password, date_joined):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_name = user_name
        self.password = password
        self.date_joined = date_joined

    def add_user(self):
        print("----Add User----\n")
        users = []
        add_more = True

        while add_more:
            user_first_name = input("Enter First Name: ")
            while not is_valid_name(user_first_name):
                user_first_name = input("Enter First Name: ")
            user_first_name = format_name(user_first_name)

            user_last_name = format_name(input("Enter Last Name: "))
            while not is_valid_name(user_last_name):
                user_last_name = input("Enter Last Name: ")
            user_last_name = format_name(user_last_name)

            user_email = input("Enter Email: ")
            while not is_valid_email(user_email):
                user_email = input("Enter Email: ")

            user_user_name = input("Enter User Name: ")
            while not is_valid_user_name(user_user_name):
                user_user_name = input("Enter User Name: ")

            user_password = input("Enter Password: ")
            while not is_valid_password(user_password):
                user_password = input("Enter Password: ")

            confirm_password = input("Confirm Password: ")
            while not valid_passwords(user_password, confirm_password):
                user_password = input("Enter Password: ")
                while not is_valid_password(user_password):
                    user_password = input("Enter Password: ")

                confirm_password = input("Confirm Password: ")

            now = datetime.datetime.now()
            date_added = now.strftime("%d-%m-%Y")
            new_user = User(user_first_name, user_last_name, user_user_name, user_email, user_password, date_added)
            users.append(new_user)
            response = input("\nAdd another user (Y/N): ").lower()
            if response == 'n':
                add_more = False

        db.insert_multiple_user(users)
        if len(users) > 1:
            print('Users have been added.\n')
        else:
            print('User has been added.\n')
        Console.clear_screen(2)
        show_admin_menu(self)

    def view_users(self):
        user_list = self.user_list('Select a user to view their details. To go back enter "/back"', True)
        if len(user_list) < 1:
            print("You currently don't have any user registered.\n")
            action = input("--> ")
            while action != '/back':
                print("\nError: Invalid input")
            Console.clear_screen(0)
            show_admin_menu(self)

        while True:
            action = input("--> ")
            if action == '/back':
                Console.clear_screen(0)
                show_admin_menu(self)
            elif re.match(r'^\d+$', action):
                selected_index = int(action)
                selected_user = user_list[selected_index - 1]
                Console.clear_screen(0)
                self.view_user_detail(selected_user)
            else:
                print("\nError: Invalid input")

    def user_list(self, message, show_list):
        print("----Users List----")
        print(message)
        user_tuple = db.get_all_users()
        user_list = []

        index = 1
        for i in user_tuple:
            user = User(i[1], i[2], i[3], i[4], i[5], i[6])
            user_list.append(user)

        if show_list:
            for user in user_list:
                print(f'{index}. {user.first_name} {user.last_name}')
                index += 1
            print()
        return user_list

    def delete_user(self):
        print('----Delete User----\n')
        print('1. Delete user from list\n2. Delete user by user name\n3. Back')

        action = input('--> ')
        while not re.match(r'^[1-3]$', action):
            print('\nInvalid input. Try again\n')
            action = input('--> ')

        if action == '1':
            Console.clear_screen(1)
            user_list = self.user_list('Select a user to delete. To go back enter "/back"', True)
            if len(user_list) < 1:
                print("You currently don't have any user registered.\n")
                action = input("--> ")
                while action != '/back':
                    action = input("--> ")
                    print("\nError: Invalid input")
                self.delete_user()
            else:
                selected_index = input('--> ')
                while int(selected_index) > len(user_list):
                    print('\nNo user found at selected index\n')
                    selected_index = input('--> ')
                user_to_delete = user_list[int(selected_index) - 1]
                print(f'\nDelete {user_to_delete.user_name}\nAre you sure you want to delete this user?(Y/N)')
                choice = input('--> ').lower()
                while choice != 'n' and choice != 'y':
                    print('\nInvalid input.\n')
                    choice = input('--> ').lower()

                if choice == 'y':
                    db.delete_user(user_to_delete)
                    print('Deleted successfully.')
                    Console.clear_screen(2)
                    self.show_dashboard()
                else:
                    Console.clear_screen(1)
                    self.delete_user()

        elif action == '2':
            Console.clear_screen(1)
            user_list = self.user_list('Delete user by user name. To go back enter "/back"', False)
            user_name = input('Enter user name of User: ')

            found = False
            for i in range(len(user_list)):
                if user_list[i].user_name == user_name:
                    user_to_delete = user_list[i]
                    db.delete_user(user_to_delete)
                    found = True
                    break

            if not found:
                print(f'User with the user name {user_name} not found.')
                Console.clear_screen(1)
                self.delete_user()
        else:
            Console.clear_screen(1)
            self.show_dashboard()

    def show_dashboard(self):
        print('----Account Details----\n')
        print(f'Admin ID: {self.id}')
        print(f'First Name: {self.first_name}')
        print(f'Last Name: {self.last_name}')
        print(f'User Name: {self.user_name}')
        print(f'Email: {self.email}')
        print('Password: ' + '*' * len(self.password))
        print(f'Date Joined: {self.date_joined}')

        print('\n1. Change User Name\n2. Change Password\n3. Change Email\n4. Delete Account\n5. Back\n')
        action = input('--> ')
        while not re.match(r'^[1-6]$', action):
            print('Invalid input. Try again')
            action = input("--> ")

        if action == '1':
            Console.clear_screen(0)
            self.change_user_name()
        elif action == '2':
            Console.clear_screen(0)
            self.change_password()
        elif action == '3':
            Console.clear_screen(0)
            self.change_email()
        elif action == '4':
            Console.clear_screen(0)
            self.delete_account()
        elif action == '5':
            Console.clear_screen(0)
            show_admin_menu(self)

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

            print(incorrect_message)
            attempts_left -= 1
            current_password = input('Enter current password: ')
            if current_password == '/back':
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
        db.update_admin_password(self)
        print('Password changed.')
        Console.clear_screen(3)
        self.show_dashboard()

    def change_user_name(self):
        print('----Change User Name----')
        print('To go back enter "/back"\n')
        print(f'Current User Name: {self.user_name}\n')
        new_user_name = input('Enter new user name: ')
        if new_user_name == '/back':
            self.show_dashboard()

        while not is_valid_user_name(new_user_name):
            new_user_name = input('Enter new user name: ')

        password = input('Enter password to confirm change: ')
        while password != self.password:
            print('\nWrong password!\n')
            password = input('Enter password to confirm change: ')

        self.user_name = new_user_name
        db.update_admin_user_name(self)

        print('\nUser Name changed.')
        Console.clear_screen(3)
        self.show_dashboard()

    def change_email(self):
        print('----Change Email----')
        print('To go back enter "/back"\n')
        print(f'Current Email: {self.email}\n')
        new_email = input('Enter new email address: ')
        if new_email == '/back':
            self.show_dashboard()

        while not is_valid_email(new_email):
            new_email = input('Enter new email address: ')

        password = input('Enter password to confirm change: ')
        while password != self.password:
            print('\nWrong password!\n')
            password = input('Enter password to confirm change: ')

        self.email = new_email
        db.update_admin_email(self)

        print('\nEmail changed.')
        Console.clear_screen(3)
        self.show_dashboard()

    def delete_account(self):
        print('----Delete Account----')
        print('To go back enter "/back"\n')
        print(f'User ID: {self.id}\nEnter User ID above to delete this account.')
        action = input('--> ')

        while action != self.id and action != '/back':
            print('\nInvalid input\n')
            action = input('--> ')

        if action == self.id:
            db.delete_admin(self)
            print('Account deleted!')
            Console.clear_screen(5)

        elif action == '/back':
            show_admin_menu(self)

    def logout(self):
        from App import show_main_menu
        show_main_menu()

    def view_user_detail(self, selected_user):
        print("----User Details----\n")
        print(f'User ID: {selected_user.id}')
        print(f'First Name: {selected_user.first_name}')
        print(f'Last Name: {selected_user.last_name}')
        print(f'User Name: {selected_user.user_name}')
        print(f'Email: {selected_user.email}')
        print('Password: ', '*' * len(selected_user.password))
        print(f'Date Joined: {selected_user.date_joined}')
        action = input('\nTo go back enter "/back": ').lower()
        while action != '/back':
            action = input('To go back enter "/back": ').lower()
        Console.clear_screen(0)
        self.view_users()
