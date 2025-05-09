from src.decorators import screen
import src.mariadb_connector as db
from src.screens.signup import sign_up
from src.screens.signin import sign_in_admin, sign_in_member, sign_in_organization

@screen
def welcome():
    print("STUDENT ORGANIZATION MANAGEMENT SYSTEM")
    print("[1] Log in as Admin")
    print("[2] Log in as Organization")
    print("[3] Log in as Member ")
    print("[4] Sign up")
    print("[5] Exit")

    user_input = input("Enter option: ")

    if user_input == "1":
        sign_in_admin()
    if user_input == "2":
        sign_in_organization()
    if user_input == "3":
        sign_in_member()
    if user_input == "4":
        sign_up()
    if user_input == "5":
        return
    
    if user_input == "test":
        db.cursor.execute("SELECT * FROM MEMBER")
        row = db.cursor.fetchall()
        print(row)