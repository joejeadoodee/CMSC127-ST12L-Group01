from src.decorators import screen
import src.mariadb_connector as db
from src import organization, navigate

@screen
def view_reports():
    while True:
        print("VIEW REPORTS")
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

        if user_input == '1':
            member_overview()
        elif user_input == '2':
            unpaid_members()
        elif user_input == '3':
            executive_committee()
        elif user_input == '4':
            historical_roles()
        elif user_input == '5':
            late_payments()
        elif user_input == '6':
            member_status_analytics()
        elif user_input == '7':
            alumni_report()
        elif user_input == '8':
            financial_summary()
        elif user_input == '9':
            member_with_highest_debt()
        elif user_input == '0':
            return navigate.to_home('organization')
        else:
            print("Invalid input. Please try again.")

@screen
def member_overview():
    print("MEMBER OVERVIEW")
    # insert code here
    input("Press Enter to return...")

@screen
def unpaid_members():
    print("UNPAID MEMBERS")
    # insert code here
    input("Press Enter to return...")

@screen
def executive_committee():
    print("EXECUTIVE COMMITTEE")
    # insert code here
    input("Press Enter to return...")

@screen
def historical_roles():
    print("HISTORICAL ROLES")
    # insert code here
    input("Press Enter to return...")

@screen
def late_payments():
    print("LATE PAYMENTS")
    # insert code here
    input("Press Enter to return...")

@screen
def member_status():
    print("MEMBER STATUS")
    # insert code here
    input("Press Enter to return...")

@screen
def alumni_report():
    print("ALUMNI REPORT")
    # insert code here
    input("Press Enter to return...")

@screen
def financial_summary():
    print("FINANCIAL SUMMARY")
    # insert code here
    input("Press Enter to return...")

@screen
def member_with_highest_debt():
    print("MEMBER WITH HIGHEST DEBT")
    # insert code here
    input("Press Enter to return...")
