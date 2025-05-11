from src.decorators import screen
import src.mariadb_connector as db
from src import organization, navigate

@screen
def home():
    while True:
        print("WELCOME, {x}".format(x=organization.name))
        print("[1] Manage Members")
        print("[2] Manage Fees")
        print("[3] View Reports")
        print("[4] Logout")

        user_input = input("Enter option: ")
        if user_input == "1":
            navigate.to_manage_members()
        elif user_input == "2":
            navigate.to_manage_fees()
        elif user_input == "3":
            navigate.to_view_reports()
        elif user_input == "4":
            return navigate.to_welcome()
        else:
            print("Invalid input. Please try again.")

@screen
def manage_members():
    print("👥 MANAGE MEMBERS")
    print("[1] Add Member")
    print("[2] Update Member")
    print("[3] Delete Member")
    print("[4] Search Members")
    print("[5] Update Member Role/Status")
    print("[0] Back")

    user_input = input("Enter option: ")
    if user_input == '0':
        navigate.to_home('organization')

@screen
def manage_fees():
    print("💰 MANAGE FEES")
    print("[1] Add Membership Fee")
    print("[2] Update Membership Fee")
    print("[3] Delete Membership Fee")
    print("[4] View Fee Records")
    print("[5] Generate Financial Report")
    print("[0] Back")

    user_input = input("Enter option: ")
    if user_input == '0':
        navigate.to_home('organization')

@screen
def view_reports():
    print("📊 VIEW REPORTS")
    print("[1] Member Overview")
    print("[2] Unpaid Members")
    print("[3] Executive Committee")
    print("[4] Historical Roles")
    print("[5] Late Payments")
    print("[6] Member Status Analytics")
    print("[7] Alumni Report")
    print("[8] Financial Summary")
    print("[9] Member with Highest Debt")
    print("[0] Back")

    user_input = input("Enter option: ")
    if user_input == '0':
        navigate.to_home('organization')