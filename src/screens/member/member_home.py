from src.decorators import screen
import src.mariadb_connector as db
from src import member
from src import navigate

@screen
def home():
    while True:
        print("WELCOME, {x}".format(x=member.name))
        print("[1] View My Profile")
        print("[2] View My Dues")
        print("[3] View My Organizations")
        print("[4] Logout")

        user_input = input("Enter option: ")

        if user_input == "1":
            navigate.to_view_profile()
        elif user_input == "2":
            navigate.to_view_dues()
        elif user_input == "3":
            navigate.to_view_organizations()
        elif user_input == "4":
            return navigate.to_welcome()
        else:
            print("Invalid input. Please try again.")

