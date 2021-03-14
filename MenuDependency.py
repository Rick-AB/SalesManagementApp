import Console
import re


def show_admin_menu(admin):
    print(f'----Logged in as {admin.user_name}----')
    print("1. Add User\n2. Delete User\n3. View Users\n4. My Account\n5. Logout\n")
    action = input("--> ")
    while not re.match(r'^[1-5]$', action):
        print('Invalid input.')
        action = input("--> ")

    if action == '1':
        Console.clear_screen(1)
        admin.add_user()
    elif action == '2':
        Console.clear_screen(1)
        admin.delete_user()
    elif action == '3':
        Console.clear_screen(1)
        admin.view_users()
    elif action == '4':
        Console.clear_screen(1)
        admin.show_dashboard()
    elif action == '5':
        print('Logging out...')
        Console.clear_screen(2)
        admin.logout()


def show_user_menu(user):
    print(f'----Logged in as {user.user_name}----')
    print("1. Add Product\n2. Restock\n3. Delete Product\n4. View Products\n5. My Account\n6. Logout\n")
    action = input("--> ")
    while not re.match(r'^[1-6]$', action):
        print('Invalid input.')
        action = input("--> ")

    if action == '1':
        Console.clear_screen(1)
        user.add_new_product()
    elif action == '2':
        Console.clear_screen(1)
        user.restock()
    elif action == '3':
        Console.clear_screen(1)
        user.delete_product()
    elif action == '4':
        Console.clear_screen(1)
        user.view_products()
    elif action == '5':
        Console.clear_screen(1)
        user.show_dashboard()
    elif action == '6':
        print('Logging out...')
        Console.clear_screen(2)
        user.logout()


def show_login_menu():
    print("Login as...")
    print("1 - Admin\n2 - User\n3 - Back\n")
    action = input("--> ")
    while not re.match(r'^[1-3]$', action):
        print('Invalid input.')
        action = input("--> ")

    from App import login_admin, login_user
    Console.clear_screen(1)
    if action == '1':
        dummy()
        # login_admin()
    elif action == '2':
        dummy()
        # login_user()
    elif action == '3':
        pass
        # from App import show_main_menu
        # show_main_menu()


def dummy():
    print('TF')
