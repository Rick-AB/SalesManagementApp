import Console
import App
from User import User

# print('Fedfe', 'er r'*12)
# action = input('\n1. Change User Name\n2. Change Password\n3. Change Email\n4. Delete Account\n5. Go Back')
# Console.clear_screen(3)
# if action == '4':
#     print('First Name: Richard')
#     print('Last Name: Bajomo')
#     print('User Name: Rick')
#     print('Email: richy@gmail.com')
#     print('Password: **************')
#     print('Date Joined: 2021-02-02')

user = User("Richard", "Bajomo", "Rick", "richardbajomo@gmail.com", "Password", "Today")
user.change_email()


