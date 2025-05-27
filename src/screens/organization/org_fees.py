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
    name = input("Enter fee name: ")
    semester = input("Enter semester: ")
    academic_year = input("Enter academic year: ")
    
    try:
        total_due = int(input("Enter total due amount: "))
        due_date = input("Enter due date (YYYY-MM-DD): ")
    except ValueError:
        print("Invalid input. Please enter valid numbers for total due and correct date format.")
        input("Press Enter to return...")  #Prompt to return
        return

    try:
        db.cursor.execute(
            "INSERT INTO FINANCIAL_OBLIGATION (name, semester, academic_year, total_due, due_date, organization_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, semester, academic_year, total_due, due_date, organization.member_id)
        )
        db.conn.commit()
        print("Fee added successfully.")
    except Exception as e:
        print("Failed to add fee:", e)

    input("Press Enter to return...")

@screen
def update_membership_fee():
    print("UPDATE MEMBERSHIP FEE")
    fee_id = input("Enter Fee ID to update: ")
    
    try:
        new_amount = int(input("Enter new total due amount: "))  # Validate input as integer
    except ValueError:
        print("Invalid amount. Please enter a valid number.")
        input("Press Enter to return...")  # Prompt to return
        return

    # Update the fee in the database
    try:
        db.cursor.execute(
            "UPDATE FINANCIAL_OBLIGATION SET total_due = %s WHERE record_id = %s",
            (new_amount, fee_id)
        )
        
        # Check if the update affected any rows
        if db.cursor.rowcount > 0:
            db.conn.commit()
            print("Fee updated successfully.")
        else:
            print("No fee found with the provided Fee ID.")
    except Exception as e:
        print("Failed to update fee:", e)

    input("Press Enter to return...")

@screen
def delete_membership_fee():
    print("DELETE MEMBERSHIP FEE")
    fee_id = input("Enter Fee ID to delete: ")

    # Validate existence of Fee ID
    if not fee_id.isdigit():
        print("Invalid Fee ID. Please enter a numeric value.")
        input("Press Enter to return...")
        return

    # Delete the fee from the database
    try:
        db.cursor.execute(
            "DELETE FROM FINANCIAL_OBLIGATION WHERE record_id = %s",
            (fee_id,)
        )
        
        # Check if any rows were affected
        if db.cursor.rowcount > 0:
            db.conn.commit()
            print("Fee deleted successfully.")
        else:
            print("No fee found with the provided Fee ID.")
    except Exception as e:
        print("Failed to delete fee:", e)

    input("Press Enter to return...")

def view_fee_records():
    print("VIEW FEE RECORDS")

    try:
        db.cursor.execute("SELECT * FROM FINANCIAL_OBLIGATION")
        records = db.cursor.fetchall()
        
        # Check if any records were found
        if records:
            # Print table header
            print(f"{'ID':<10} {'Name':<30} {'Semester':<15} {'Academic Year':<15} {'Total Due':<15} {'Due Date':<15}")
            print("-" * 100)
            
            # Print each record in a formatted row
            for record in records:
                due_date = str(record[5])  # Directly convert due_date to string
                print(f"{record[0]:<10} {record[3]:<30} {record[1]:<15} {record[2]:<15} {record[4]:<15} {due_date:<15}")
        else:
            print("No fee records found.")
    except Exception as e:
        print("Failed to retrieve fee records:", e)

    input("Press Enter to return...")

def generate_financial_report():
    print("GENERATE FINANCIAL REPORT")
    # insert code here
    input("Press Enter to return...")
