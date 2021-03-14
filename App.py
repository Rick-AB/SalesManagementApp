from Admin import Admin
from Validator import is_valid_name, is_valid_password, valid_passwords, is_valid_email, is_valid_user_name, format_name
from User import User
from Database import Database as db
from time import sleep
import sys
import re
import Console
import datetime


# Menu definition
def show_main_menu():
    print("-----Welcome to Rick Inc-----\n")
    print("1 - Register\n2 - Log in\n3 - Exit\n")
    action = input("--> ")
    while not re.match(r'^[1-3]$', action):
        print('Invalid input.')
        action = input("--> ")

    Console.clear_screen(1)
    if action == '1':
        show_register_menu()
    elif action == '2':
        show_login_menu()
    elif action == '3':
        sys.exit(0)


def show_login_menu():
    print("Login as...")
    print("1 - Admin\n2 - User\n3 - Back\n")
    action = input("--> ")
    while not re.match(r'^[1-3]$', action):
        print('Invalid input.')
        action = input("--> ")

    Console.clear_screen(1)
    if action == '1':
        login_admin()
    elif action == '2':
        login_user()
    elif action == '3':
        show_main_menu()


def show_register_menu():
    print("Register as...")
    print("1 - Admin\n2 - User\n3 - Back\n")
    action = input("--> ")
    while not re.match(r'^[1-3]$', action):
        print('Invalid input.')
        action = input("--> ")

    Console.clear_screen(1)
    if action == '1':
        register_admin()
    elif action == '2':
        register_user()
    elif action == '3':
        show_main_menu()


def register_user():
    print("----Rick Inc Registration Form----\n")
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
    db.insert_user(new_user)
    print("Thank you for registering with us!")
    print("Redirecting to login page...")
    sleep(3)
    Console.clear_screen(3)
    login_user()


def show_user_menu(user):
    print(f'----Logged in as {user.user_name}----')
    print("1. Add Product\n2. Restock\n3. Delete Product\n4. View Products\n5. My Account\n6. Logout\n")
    action = input("--> ")
    while not re.match(r'^[1-6]$', action):
        print('Invalid input.')
        action = input("--> ")

    Console.clear_screen(1)
    if action == '1':
        user.add_new_product()
    elif action == '2':
        user.restock()
    elif action == '3':
        user.delete_product()
    elif action == '4':
        user.view_products()
    elif action == '5':
        user.show_dashboard()
    elif action == '6':
        user.logout()


def login_user():
    print("---Login as User---\n")
    email_or_user_name = input("Enter user name or email: ")
    password = input("Enter password: ")
    response, user_tuple = db.get_user(email_or_user_name, password)

    while True:
        user = None
        if user_tuple is not None:
            user = User(user_tuple[1], user_tuple[2], user_tuple[3], user_tuple[4], user_tuple[5], user_tuple[6])
            user.id = user_tuple[0]

        if "No" in response:
            print("Incorrect User Name or Email")
            email_or_user_name = input("Enter user name or email: ")
            password = input("Enter password: ")
            response, user_tuple = db.get_user(email_or_user_name, password)

        elif "Wrong" in response:
            print("Incorrect Password")
            password = input("Enter password: ")
            response, user_tuple = db.get_user(email_or_user_name, password)
        else:
            print("Logged In Successfully...")
            Console.clear_screen(2)
            show_user_menu(user)


def show_admin_menu(admin):
    print(f'----Logged in as {admin.user_name}----')
    print("1. Add User\n2. Delete User\n3. View Users\n4. My Account\n5. Logout\n")
    action = input("--> ")
    while not re.match(r'^[1-5]$', action):
        print('Invalid input.')
        action = input("--> ")

    Console.clear_screen(1)
    if action == '1':
        admin.add_user()
    elif action == '2':
        admin.delete_user()
    elif action == '3':
        admin.view_users()
    elif action == '4':
        admin.show_dashboard()
    elif action == '5':
        admin.logout()


def login_admin():
    print("----Login as Admin----\n")
    email_or_user_name = input("Enter user name or email: ")
    password = input("Enter password: ")
    response, admin_tuple = db.get_admin(email_or_user_name, password)

    while True:
        admin = None
        if admin_tuple is not None:
            admin = Admin(admin_tuple[1], admin_tuple[2], admin_tuple[3], admin_tuple[4], admin_tuple[5],
                          admin_tuple[6])
            admin.id = admin_tuple[0]

        if "No" in response:
            print("Incorrect User Name or Email")
            email_or_user_name = input("Enter user name or email: ")
            password = input("Enter password: ")
            response, admin_tuple = db.get_admin(email_or_user_name, password)

        elif "Wrong" in response:
            print("Incorrect Password")
            password = input("Enter password: ")
            response, admin_tuple = db.get_admin(email_or_user_name, password)
        elif "Correct" in response:
            print("Logged In Successfully...")
            Console.clear_screen(2)
            show_admin_menu(admin)


def register_admin():
    print("----Rick Inc Registration Form----\n")
    admin_first_name = input("Enter First Name: ")
    while not is_valid_name(admin_first_name):
        admin_first_name = input("Enter First Name: ")
    admin_first_name = format_name(admin_first_name)

    admin_last_name = format_name(input("Enter Last Name: "))
    while not is_valid_name(admin_last_name):
        admin_last_name = input("Enter Last Name: ")
    admin_last_name = format_name(admin_last_name)

    admin_email = input("Enter Email: ")
    while not is_valid_email(admin_email):
        admin_email = input("Enter Email: ")

    admin_user_name = input("Enter User Name: ")
    while not is_valid_user_name(admin_user_name):
        admin_user_name = input("Enter User Name: ")

    admin_password = input("Enter Password: ")
    while not is_valid_password(admin_password):
        admin_password = input("Enter Password: ")

    confirm_password = input("Confirm Password: ")
    while not valid_passwords(admin_password, confirm_password):
        admin_password = input("Enter Password: ")
        while not is_valid_password(admin_password):
            admin_password = input("Enter Password: ")

        confirm_password = input("Confirm Password: ")

    now = datetime.datetime.now()
    date_added = now.strftime("%d-%m-%Y")

    new_admin = Admin(admin_first_name, admin_last_name, admin_user_name, admin_email, admin_password, date_added)
    db.insert_admin(new_admin)
    print("Thank you for registering with us!")
    print("Redirecting to login page...")
    sleep(3)
    Console.clear_screen(3)
    login_admin()


# Beginning of program
show_main_menu()
