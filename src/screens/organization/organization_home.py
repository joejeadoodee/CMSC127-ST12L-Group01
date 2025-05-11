from src.decorators import screen
import src.mariadb_connector as db
from src.screens.signup import sign_up
from src import organization

@screen
def home():
    print("WELCOME, {x}".format(x=organization.name))
    print("[1] Manage Members")
    print("[2] Manage Fees")
    print("[3] View Reports")
    print("[4] Logout")

    user_input = input("Enter option: ")
