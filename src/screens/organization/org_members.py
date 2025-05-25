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
    name = input("Enter new name (leave blank to keep current): ")
    student_id = input("Enter new student ID (leave blank to keep current): ")

    if db.update_member(member_id, name=name or None, student_id=student_id or None):
        print("Member updated successfully.")
    else:
        print("Member update failed.")
    input("Press Enter to return...")

@screen
def delete_member():
    print("DELETE MEMBER")
    member_id = input("Enter Member ID to delete: ")
    confirm = input("Delete this member? [Y/N]: ")

    if confirm.upper() == 'Y':
        try:
            db.cursor.execute("DELETE FROM MEMBER WHERE member_id = ?", (member_id,))
            if db.cursor.rowcount == 0:
                print("No member found with that ID.")
            else:
                db.conn.commit()
                print("Member deleted successfully.")
        except Exception as e:
            print("An error occurred while deleting the member: ", e)
    else:
        print("Deletion cancelled.")
    input("Press Enter to return...")

@screen
def search_members():
    print("SEARCH MEMBERS")
    query = input("Enter name, ID, or keyword: ")
    
    try: 
        search_query = f"%{query}%"
        db.cursor.execute("""
            SELECT member_id, name, student_id, status 
            FROM MEMBER 
            WHERE name LIKE ? OR student_id LIKE ?
        """, (search_query, search_query))
        results = db.cursor.fetchall()

        if not results:
            print("No matching members found.")
        else:
            print("\nMATCHING MEMBERS: ")
            for member in results:
                print(f"ID: {member[0]} | Name: {member[1]} | Student ID: {member[2]} | Status: {member[3]}")
    except Exception as e:
        print("Error while searching members: ", e)
    input("Press Enter to return...")

@screen
def update_member_role_status():
    print("UPDATE MEMBER ROLE/STATUS")
    member_id = input("Enter Member ID: ")
    role = input("Enter new role: ")
    status = input("Enter new status: ")

    try:
        db.cursor.execute("""
            UPDATE SERVES 
            SET role = ?, semester = semester, school_year = school_year 
            WHERE member_id = ?
        """, (role, member_id))
        
        db.cursor.execute("""
            UPDATE MEMBER 
            SET status = ?
            WHERE member_id = ?
        """, (status, member_id))

        if db.cursor.rowcount == 0:
            print("No member found with that ID.")
        else:
            db.conn.commit()
            print("Member role/status updated successfully.")
    except Exception as e:
        print("Error while updating member role/status: ", e)
    input("Press Enter to return...")
