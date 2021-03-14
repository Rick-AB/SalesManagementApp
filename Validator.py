import re


def format_name(name):
    return name[0].capitalize() + name[1:]


def is_valid_name(name):
    has_space = re.compile(r'\w*\s+')
    has_digits = re.compile(r'\w*\d+')
    has_special_characters = re.compile(r'[~!@#$%^&*()_+=:;,.?`]+')

    if has_special_characters.match(name):
        print("\nError: Name cannot contain special characters\n")
        return False
    if has_space.match(name):
        print("\nError: Name should not contain space.\n")
        return False
    if has_digits.match(name):
        print("\nError: Name should not contain digits.\n")
        return False
    if len(name) == 0:
        print("\nError: Name cannot be empty.\n")
        return False
    return True


def is_valid_password(password):
    uppercase_regex = re.compile(r'.*[A-Z]+')
    lowercase_regex = re.compile(r'.*[a-z]+')
    eight_characters = re.compile(r'.{8,}')
    contains_space = re.compile(r'.*\s+')

    if not uppercase_regex.search(password):
        print("\nError: Password must have at least one uppercase letter.\n")
        return False
    if not lowercase_regex.match(password):
        print("\nError: Password must have at least one lowercase letter.\n")
        return False
    if not eight_characters.match(password):
        print("\nError: Password must be at least eight characters long.\n")
        return False
    if contains_space.match(password):
        print("\nError: Password cannot contain spaces.\n")
        return False

    return True


def valid_passwords(password, confirm_password):
    if not (password == confirm_password):
        print("\nError: Passwords do not match.\n")
        return False
    else:
        return True


def is_valid_email(email):
    contains_at_symbol = re.compile(r'[A-Za-z0-9+_~!#$%&=?]+@')
    contains_domain = re.compile(r'.+@[\w]+[.]com')

    if not contains_at_symbol.match(email):
        print("\nError: Invalid Email (No @ symbol)\n")
        return False
    if not contains_domain.match(email):
        print("\nError: Invalid Email (Incorrect domain format)\n")
        return False
    return True


def is_valid_user_name(user_name):
    if len(user_name) == 0:
        print("\nError: User Name cannot be empty.\n")
        return False
    return True


def is_valid_product_name(name):
    all_spaces_regex = re.compile(r'\s+')

    if len(name) < 3:
        print("\nError: Product name should contain at least 3 characters\n")
        return False
    elif all_spaces_regex.match(name):
        print("\nError: Product name cannot be all spaces\n")
        return False
    else:
        return True


def is_valid_product_category(category):
    all_spaces_regex = re.compile(r'\s+')
    has_digits = re.compile(r'\w*\d+')

    if len(category) < 3:
        print("\nError: Product category should contain at least 3 characters\n")
        return False
    elif all_spaces_regex.match(category):
        print("\nError: Product category cannot be all spaces\n")
        return False
    elif has_digits.match(category):
        print("\nError: Product category cannot contain digits\n")
    else:
        return True


def is_valid_price(price):
    only_digits = re.compile(r'^\d+$')

    if not only_digits.match(price):
        print("\nError: Product price must be all digits\n")
        return False
    else:
        return True


def is_valid_quantity(quantity):
    only_digits = re.compile(r'^\d+$')

    if not only_digits.match(quantity):
        print("\nError: Product quantity must be all digits\n")
        return False
    else:
        return True
