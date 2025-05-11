from src.decorators import screen
import src.mariadb_connector as db
from src.screens.signup import sign_up

@screen
def home():
    print("WELCOME, ADMIN")
    print("[1] Manage All Members")
    print("[2] Manage Organizations")
    print("[3] View Membership Reports")
    print("[4] View Financial Reports")
    print("[6] Logout")

    user_input = input("Enter option: ")
