from src.decorators import screen
import src.mariadb_connector as db
from src import organization, navigate

@screen
def manage_fees():
    while True:
        print("MANAGE FEES")
        print("[1] Add Membership Fee")
        print("[2] Update Membership Fee")
        print("[3] Delete Membership Fee")
        print("[4] View Fee Records")
        print("[5] Generate Financial Report")
        print("[0] Back")

        user_input = input("Enter option: ")

        if user_input == '1':
            add_membership_fee()
        elif user_input == '2':
            update_membership_fee()
        elif user_input == '3':
            delete_membership_fee()
        elif user_input == '4':
            view_fee_records()
        elif user_input == '5':
            generate_financial_report()
        elif user_input == '0':
            return navigate.to_home('organization')
        else:
            print("Invalid input. Please try again.")

@screen
def add_membership_fee():
    print("ADD MEMBERSHIP FEE")
    description = input("Enter fee description: ")
    amount = input("Enter amount: ")
    # insert code here
    input("Press Enter to return...")

@screen
def update_membership_fee():
    print("UPDATE MEMBERSHIP FEE")
    fee_id = input("Enter Fee ID to update: ")
    new_amount = input("Enter new amount: ")
    # insert code here
    input("Press Enter to return...")

@screen
def delete_membership_fee():
    print("DELETE MEMBERSHIP FEE")
    fee_id = input("Enter Fee ID to delete: ")
    # insert code here
    input("Press Enter to return...")

def view_fee_records():
    print("VIEW FEE RECORDS")
    # insert code here
    input("Press Enter to return...")

def generate_financial_report():
    print("GENERATE FINANCIAL REPORT")
    # insert code here
    input("Press Enter to return...")
