from src.decorators import screen
import src.mariadb_connector as db
from src import member, navigate

@screen
def view_dues():
    while True:
        print("MY DUES")
        print("[1] View All Dues")
        print("[2] Pay a Due")
        print("[3] View Payment History")
        print("[0] Back")

        user_input = input("Enter option: ")

        if user_input == "1":
            view_all_dues()
        elif user_input == "2":
            pay_due()
        elif user_input == "3":
            view_payment_history()
        elif user_input == "0":
            return navigate.to_home('member')

        else:
            print("Invalid input. Please try again.")

@screen
def view_all_dues():
    print("MY DUES")
    # insert code here

@screen
def pay_due():
    print("PAY DUE")
    # insert code here

@screen
def view_payment_history():
    print("MY PAYMENT HISTORY")
    # insert code here

