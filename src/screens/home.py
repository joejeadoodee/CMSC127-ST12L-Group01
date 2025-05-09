from src.decorators import screen
import src.mariadb_connector as db
from src.screens.signup import sign_up
from src import provider

@screen
def home():
    print("WELCOME, {x}".format(x=provider.name))
    print("[1] View Profile")

    user_input = input("Enter option: ")