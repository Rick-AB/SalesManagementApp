import sqlite3


def create_connection():
    connection = None
    try:
        connection = sqlite3.connect("SalesManagement.sqlite3")

    except sqlite3.Error as e:
        print(e)

    return connection


def insert_user(user):
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    email = user.email
    user_name = user.user_name
    password = user.password
    date_joined = user.date_joined

    user_info = (user_id, first_name, last_name, user_name, email, password, date_joined)

    db = create_connection()
    if db is not None:
        with db:
            table_statement = "CREATE TABLE IF NOT EXISTS User(Id TEXT PRIMARY KEY, First_Name TEXT, Last_Name " \
                              "TEXT, User_Name TEXT UNIQUE, Email TEXT UNIQUE, Password TEXT, Date_Joined TEXT) "

            insert_statement = "INSERT INTO User(Id, First_Name, Last_Name, User_Name, Email, Password, Date_Joined) " \
                               "VALUES(?,?,?,?,?,?,?) "
            cursor = db.cursor()
            cursor.execute(table_statement)
            try:
                cursor.execute(insert_statement, user_info)
                db.commit()
                cursor.close()
            except sqlite3.IntegrityError as e:
                print(e)

    else:
        print("==========Error Connecting to Database==========")


def insert_products(products):
    db = create_connection()
    if db is not None:
        with db:
            table_statement = "CREATE TABLE IF NOT EXISTS Product(Id TEXT PRIMARY KEY, Owner_Id TEXT, Name TEXT, " \
                              "Category TEXT, Price TEXT, Quantity TEXT, Date_Added TEXT) "

            insert_statement = "INSERT INTO Product(Id, Owner_Id, Name, Category, Price, Quantity, Date_Added) " \
                               "VALUES(?,?,?,?,?,?,?)"
            cursor = db.cursor()
            cursor.execute(table_statement)

            for product in products:
                product_id = product.product_id
                owner_id = product.owner_id
                name = product.name
                category = product.category
                price = product.price
                quantity = product.quantity
                date_added = product.date_added
                product_info = (product_id, owner_id, name, category, price, quantity, date_added)

                cursor.execute(insert_statement, product_info)
                db.commit()

            cursor.close()

    else:
        print("==========Error Connecting to Database==========")


def get_user(login, password):
    user_info = login
    db = create_connection()
    if db is not None:
        with db:
            if "@" in login:
                select_user_statement = "SELECT * FROM User WHERE Email = ?"
            else:
                select_user_statement = "SELECT * FROM User WHERE User_Name = ?"

            cursor = db.cursor()
            cursor.execute(select_user_statement, (user_info,))

            rows = cursor.fetchall()
            if len(rows) < 1:
                return "No User Found", None
            else:
                user_tuple = rows[0]
                if user_tuple[5] == password:
                    return "Correct Password", user_tuple
                else:
                    return "Wrong Password", None

    else:
        print("==========Error Connecting to Database==========")
        return "", None


def get_all_product(owner_id):
    db = create_connection()

    if db is not None:
        with db:
            table_statement = "CREATE TABLE IF NOT EXISTS Product(Id TEXT PRIMARY KEY, Owner_Id TEXT, Name TEXT, " \
                              "Category TEXT, Price TEXT, Quantity TEXT, Date_Added TEXT) "

            select_statement = "SELECT * FROM Product WHERE Owner_Id = ?"
            cursor = db.cursor()
            cursor.execute(table_statement)
            cursor.execute(select_statement, (owner_id,))
            rows = cursor.fetchall()
            result_list = []
            for i in rows:
                result_list.append(i)
            return result_list

    else:
        print("==========Error Connecting to Database==========")


def update_user_user_name(user):
    user_info = (user.user_name, user.id)
    db = create_connection()
    if db is not None:
        with db:
            table_statement = "CREATE TABLE IF NOT EXISTS User(Id TEXT PRIMARY KEY, First_Name TEXT, Last_Name " \
                              "TEXT, User_Name TEXT UNIQUE, Email TEXT UNIQUE, Password TEXT, Date_Joined TEXT) "

            update_statement = "UPDATE User SET User_Name = ? WHERE Id = ?"
            cursor = db.cursor()
            cursor.execute(table_statement)
            cursor.execute(update_statement, user_info)
            db.commit()
            cursor.close()

    else:
        print("==========Error Connecting to Database==========")


def update_user_password(user):
    user_info = (user.password, user.id)
    db = create_connection()
    if db is not None:
        with db:
            table_statement = "CREATE TABLE IF NOT EXISTS User(Id TEXT PRIMARY KEY, First_Name TEXT, Last_Name " \
                              "TEXT, User_Name TEXT UNIQUE, Email TEXT UNIQUE, Password TEXT, Date_Joined TEXT) "

            update_statement = "UPDATE User SET Password = ? WHERE Id = ?"
            cursor = db.cursor()
            cursor.execute(table_statement)
            cursor.execute(update_statement, user_info)
            db.commit()
            cursor.close()

    else:
        print("==========Error Connecting to Database==========")


def update_user_email(user):
    user_info = (user.email, user.id)
    db = create_connection()
    if db is not None:
        with db:
            table_statement = "CREATE TABLE IF NOT EXISTS User(Id TEXT PRIMARY KEY, First_Name TEXT, Last_Name " \
                              "TEXT, User_Name TEXT UNIQUE, Email TEXT UNIQUE, Password TEXT, Date_Joined TEXT) "

            update_statement = "UPDATE User SET Email = ? WHERE Id = ?"
            cursor = db.cursor()
            cursor.execute(table_statement)
            cursor.execute(update_statement, user_info)
            db.commit()
            cursor.close()

    else:
        print("==========Error Connecting to Database==========")


def restock_product(product):
    product_info = (product.quantity, product.product_id)
    db = create_connection()
    if db is not None:
        with db:
            table_statement = "CREATE TABLE IF NOT EXISTS Product(Id TEXT PRIMARY KEY, Owner_Id TEXT, Name TEXT, " \
                              "Category TEXT, Price TEXT, Quantity TEXT, Date_Added TEXT) "

            update_statement = "UPDATE Product SET Quantity = ? WHERE Id = ?"
            cursor = db.cursor()
            cursor.execute(table_statement)
            cursor.execute(update_statement, product_info)
            db.commit()
            cursor.close()

    else:
        print("==========Error Connecting to Database==========")


def get_product_by_name(product_name):
    db = create_connection()
    if db is not None:
        with db:
            table_statement = "CREATE TABLE IF NOT EXISTS Product(Id TEXT PRIMARY KEY, Owner_Id TEXT, Name TEXT, " \
                              "Category TEXT, Price TEXT, Quantity TEXT, Date_Added TEXT) "

            select_statement = "SELECT * FROM Product WHERE Name = ?"
            cursor = db.cursor()
            cursor.execute(table_statement)
            cursor.execute(select_statement, (product_name,))
            rows = cursor.fetchall()

            if len(rows) > 0:
                current_product = rows[0]
                return current_product
            else:
                return None

    else:
        print("==========Error Connecting to Database==========")


def delete_user(user):
    db = create_connection()
    if db is not None:
        with db:
            table_statement = "CREATE TABLE IF NOT EXISTS User(Id TEXT PRIMARY KEY, First_Name TEXT, Last_Name " \
                              "TEXT, User_Name TEXT UNIQUE, Email TEXT UNIQUE, Password TEXT, Date_Joined TEXT) "

            delete_statement = "DELETE FROM User WHERE Id = ?"
            cursor = db.cursor()
            cursor.execute(table_statement)
            cursor.execute(delete_statement, (user.id,))
            db.commit()
            cursor.close()

    else:
        print("==========Error Connecting to Database==========")


def insert_admin(admin):
    admin_id = admin.id
    first_name = admin.first_name
    last_name = admin.last_name
    email = admin.email
    user_name = admin.user_name
    password = admin.password
    date_joined = admin.date_joined

    admin_info = (admin_id, first_name, last_name, user_name, email, password, date_joined)

    db = create_connection()
    if db is not None:
        with db:
            table_statement = "CREATE TABLE IF NOT EXISTS Admin(Id TEXT PRIMARY KEY, First_Name TEXT, Last_Name " \
                              "TEXT, User_Name TEXT UNIQUE, Email TEXT UNIQUE, Password TEXT, Date_Joined TEXT) "

            insert_statement = "INSERT INTO Admin(Id, First_Name, Last_Name, User_Name, Email, Password, Date_Joined)" \
                               " VALUES(?,?,?,?,?,?,?) "
            cursor = db.cursor()
            cursor.execute(table_statement)
            try:
                cursor.execute(insert_statement, admin_info)
                db.commit()
                cursor.close()
            except sqlite3.IntegrityError as e:
                print(e)

    else:
        print("==========Error Connecting to Database==========")


def get_admin(login, password):
    admin_info = login
    db = create_connection()
    if db is not None:
        with db:
            if "@" in login:
                select_admin_statement = "SELECT * FROM Admin WHERE Email = ?"
            else:
                select_admin_statement = "SELECT * FROM Admin WHERE User_Name = ?"

            cursor = db.cursor()
            cursor.execute(select_admin_statement, (admin_info,))

            rows = cursor.fetchall()
            if len(rows) < 1:
                return "No Admin Found", None
            else:
                admin_tuple = rows[0]
                if admin_tuple[5] == password:
                    return "Correct Password", admin_tuple
                else:
                    return "Wrong Password", None

    else:
        print("==========Error Connecting to Database==========")
        return "", None


def delete_product(product):
    db = create_connection()
    if db is not None:
        with db:
            table_statement = "CREATE TABLE IF NOT EXISTS Product(Id TEXT PRIMARY KEY, Owner_Id TEXT, Name TEXT, " \
                              "Category TEXT, Price TEXT, Quantity TEXT, Date_Added TEXT) "

            delete_statement = "DELETE FROM Product WHERE Name = ?"
            cursor = db.cursor()
            cursor.execute(table_statement)
            cursor.execute(delete_statement, (product.name,))
            db.commit()
            cursor.close()

    else:
        print("==========Error Connecting to Database==========")


def insert_multiple_user(users):
    db = create_connection()
    if db is not None:
        with db:
            table_statement = "CREATE TABLE IF NOT EXISTS User(Id TEXT PRIMARY KEY, First_Name TEXT, Last_Name " \
                              "TEXT, User_Name TEXT UNIQUE, Email TEXT UNIQUE, Password TEXT, Date_Joined TEXT) "

            insert_statement = "INSERT INTO User(Id, First_Name, Last_Name, User_Name, Email, Password, Date_Joined) " \
                               "VALUES(?,?,?,?,?,?,?) "
            cursor = db.cursor()
            cursor.execute(table_statement)

            for user in users:
                user_id = user.id
                first_name = user.first_name
                last_name = user.last_name
                user_name = user.user_name
                email = user.email
                password = user.password
                date_joined = user.date_joined
                user_info = (user_id, first_name, last_name, user_name, email, password, date_joined)

                cursor.execute(insert_statement, user_info)
                db.commit()

            cursor.close()

    else:
        print("==========Error Connecting to Database==========")


def get_all_users():
    db = create_connection()

    if db is not None:
        with db:
            table_statement = "CREATE TABLE IF NOT EXISTS User(Id TEXT PRIMARY KEY, First_Name TEXT, Last_Name " \
                              "TEXT, User_Name TEXT UNIQUE, Email TEXT UNIQUE, Password TEXT, Date_Joined TEXT) "

            select_statement = "SELECT * FROM User"
            cursor = db.cursor()
            cursor.execute(table_statement)
            cursor.execute(select_statement)
            rows = cursor.fetchall()
            result_list = []
            for i in rows:
                result_list.append(i)
            return result_list

    else:
        print("==========Error Connecting to Database==========")


def update_admin_password(admin):
    admin_info = (admin.password, admin.id)
    db = create_connection()
    if db is not None:
        with db:
            table_statement = "CREATE TABLE IF NOT EXISTS Admin(Id TEXT PRIMARY KEY, First_Name TEXT, Last_Name " \
                              "TEXT, User_Name TEXT UNIQUE, Email TEXT UNIQUE, Password TEXT, Date_Joined TEXT) "

            update_statement = "UPDATE Admin SET Password = ? WHERE Id = ?"
            cursor = db.cursor()
            cursor.execute(table_statement)
            cursor.execute(update_statement, admin_info)
            db.commit()
            cursor.close()

    else:
        print("==========Error Connecting to Database==========")


def delete_admin(admin):
    db = create_connection()
    if db is not None:
        with db:
            table_statement = "CREATE TABLE IF NOT EXISTS Admin(Id TEXT PRIMARY KEY, First_Name TEXT, Last_Name " \
                              "TEXT, User_Name TEXT UNIQUE, Email TEXT UNIQUE, Password TEXT, Date_Joined TEXT) "

            delete_statement = "DELETE FROM Admin WHERE Id = ?"
            cursor = db.cursor()
            cursor.execute(table_statement)
            cursor.execute(delete_statement, (admin.id,))
            db.commit()
            cursor.close()

    else:
        print("==========Error Connecting to Database==========")


def update_admin_user_name(admin):
    admin_info = (admin.user_name, admin.id)
    db = create_connection()
    if db is not None:
        with db:
            table_statement = "CREATE TABLE IF NOT EXISTS Admin(Id TEXT PRIMARY KEY, First_Name TEXT, Last_Name " \
                              "TEXT, User_Name TEXT UNIQUE, Email TEXT UNIQUE, Password TEXT, Date_Joined TEXT) "

            update_statement = "UPDATE Admin SET User_Name = ? WHERE Id = ?"
            cursor = db.cursor()
            cursor.execute(table_statement)
            cursor.execute(update_statement, admin_info)
            db.commit()
            cursor.close()

    else:
        print("==========Error Connecting to Database==========")


def update_admin_email(admin):
    admin_info = (admin.email, admin.id)
    db = create_connection()
    if db is not None:
        with db:
            table_statement = "CREATE TABLE IF NOT EXISTS Admin(Id TEXT PRIMARY KEY, First_Name TEXT, Last_Name " \
                              "TEXT, User_Name TEXT UNIQUE, Email TEXT UNIQUE, Password TEXT, Date_Joined TEXT) "

            update_statement = "UPDATE Admin SET Email = ? WHERE Id = ?"
            cursor = db.cursor()
            cursor.execute(table_statement)
            cursor.execute(update_statement, admin_info)
            db.commit()
            cursor.close()

    else:
        print("==========Error Connecting to Database==========")
