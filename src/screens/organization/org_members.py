from src.decorators import screen
import src.mariadb_connector as db
from src import organization, navigate

@screen
def manage_members():
    while True:
        print("MANAGE MEMBERS")
        print("[1] Add Member")
        print("[2] Update Member")
        print("[3] Delete Member")
        print("[4] Search Members")
        print("[5] Update Member Role/Status")
        print("[0] Back")

        user_input = input("Enter option: ")

        if user_input == '1':
            add_member()
        elif user_input == '2':
            update_member()
        elif user_input == '3':
            delete_member()
        elif user_input == '4':
            search_members()
        elif user_input == '5':
            update_member_role_status()
        elif user_input == '0':
            return navigate.to_home('organization')
        else:
            print("Invalid input. Please try again.")

@screen
def add_member():
    print("ADD MEMBER")
    name = input("Enter full name: ")
    student_id = input("Enter student ID: ")
    
    if not name or not student_id:
        print("Invalid input. Name and student ID are required.")
    else:
        if db.add_member(name, student_id):
            print("Member added successfully.")
        else:
            print("Failed to add member.")
    input("Press Enter to return...")

@screen
def update_member():
    print("UPDATE MEMBER")
    member_id = input("Enter Member ID to update: ")
    
    input("Press Enter to return...")

@screen
def delete_member():
    print("DELETE MEMBER")
    member_id = input("Enter Member ID to delete: ")
    # insert code here
    input("Press Enter to return...")

@screen
def search_members():
    print("SEARCH MEMBERS")
    query = input("Enter name, ID, or keyword: ")
    # insert code here
    input("Press Enter to return...")

@screen
def update_member_role_status():
    print("UPDATE MEMBER ROLE/STATUS")
    member_id = input("Enter Member ID: ")
    role = input("Enter new role: ")
    status = input("Enter new status: ")
    # insert code here
    input("Press Enter to return...")
