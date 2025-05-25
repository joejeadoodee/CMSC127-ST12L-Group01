import datetime
from src.decorators import screen
import src.mariadb_connector as db
from src import member, navigate
from tabulate import tabulate

current_record_id = None

@screen
def view_dues():
    while True:
        print("FINANCIAL OBLIGATIONS")
        print("[1] Settle Dues")
        print("[2] View Payment History")
        print("[0] Back")

        user_input = input("Enter option: ")

        if user_input == "1":
            view_all_dues()
        elif user_input == "2":
            view_payment_history()
        elif user_input == "0":
            return navigate.to_home('member')

        else:
            print("Invalid input. Please try again.")


def create_table(rows, headers, message):
    tables = {}

    for row in rows:
        obligation_name = row[4]
        organization_name = row[2]
        academic_year = row[6]
        semester = row[5]
        total_amount_paid = row[9]
        total_due = row[7]

        if organization_name in tables:
            tables[organization_name].append([
                obligation_name, academic_year, semester, total_amount_paid, total_due
            ])
        else:
            tables[organization_name] = [[
                obligation_name, academic_year, semester, total_amount_paid, total_due
            ]]

    for key, value in tables.items():
        print(f"    {key}")
        table_str = tabulate(value, headers=headers, tablefmt="fancy_grid")
        indented_table = "\n".join([f"      {line}" for line in table_str.splitlines()])
        print(indented_table)

    if len(tables.items()) == 0:
        print(f"    {message}")
        return False
    
    return True


@screen
def view_all_dues():
    print("MY PENDING DUES\n")
    member_id = member.member_id

    db.cursor.execute(f"""
        SELECT * FROM (
            SELECT s.member_id, m.username, o.name, f.record_id, f.name as `obligation_name`, f.semester, f.academic_year, f.total_due, f.due_date, 
            COALESCE(p.total_amount_paid, 0) as `total_amount_paid`
            FROM SERVES s
            LEFT JOIN MEMBER m
            ON s.member_id=m.member_id
            LEFT JOIN ORGANIZATION o
            ON o.organization_id=s.organization_id
            LEFT JOIN FINANCIAL_OBLIGATION f
            ON o.organization_id=f.organization_id
            LEFT JOIN (
                SELECT record_id, member_id, SUM(amount_paid) `total_amount_paid`
                FROM PAYMENT p
                GROUP BY record_id, member_id
            ) p
            ON f.record_id=p.record_id AND s.member_id=p.member_id
            WHERE s.member_id = {member_id}
            ORDER BY s.member_id, o.name, f.name
        ) result WHERE total_amount_paid < total_due;
    """)
    
    
    rows = db.cursor.fetchall()

    headers = ["Record id", "Organization", "Obligation", "Academic Year", "Semester", "Amount Paid", "Total Due"]

    result = []

    for row in rows:
        record_id = row[3]
        obligation_name = row[4]
        organization_name = row[2]
        academic_year = row[6]
        semester = row[5]
        total_amount_paid = row[9]
        total_due = row[7]
        result.append([record_id, organization_name, obligation_name, academic_year, semester, total_amount_paid, total_due])
        

    table_str = tabulate(result, headers=headers, tablefmt="fancy_grid")
    indented_table = "\n".join([f"      {line}" for line in table_str.splitlines()])
    print(indented_table)



@screen
def view_payment_history():
    print("MY PAYMENT HISTORY\n")
    member_id = member.member_id

    db.cursor.execute(f"""
        SELECT p.payment_id, o.name, f.name, p.amount_paid, p.payment_date
        FROM PAYMENT p 
        LEFT JOIN FINANCIAL_OBLIGATION f
        ON f.record_id=p.record_id
        LEFT JOIN ORGANIZATION o
        ON f.organization_id=o.organization_id
        WHERE p.member_id = {member_id}
        ORDER BY p.member_id, o.name, f.name, p.payment_date DESC;
    """)
    
    rows = db.cursor.fetchall()

    headers = ["Payment id", "Organization", "Obligation", "Amount Paid", "Payment date"]        

    table_str = tabulate(rows, headers=headers, tablefmt="fancy_grid")
    indented_table = "\n".join([f"      {line}" for line in table_str.splitlines()])
    print(indented_table)

    

    