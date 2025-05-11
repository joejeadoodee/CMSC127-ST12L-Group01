from src.decorators import screen
import src.mariadb_connector as db
from src.screens.signup import sign_up
from src import member

@screen
def home():
    print("WELCOME, {x}".format(x=member.name))
    print("[1] View My Profile")
    print("[2] View My Dues")
    print("[3] View My Organizations")
    print("[4] Logout")

    user_input = input("Enter option: ")