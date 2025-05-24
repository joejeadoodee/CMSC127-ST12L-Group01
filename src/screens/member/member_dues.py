import datetime
from src.decorators import screen
import src.mariadb_connector as db
from src import member, navigate
from tabulate import tabulate

current_record_id = None

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
    member_id = member.member_id

    db.cursor.execute(f"""
        SELECT osmfp.mem_id as 'member_id', osmfp.full_name, osmfp.record_id, osmfp.name as 'obligation_name', osmfp.org_id as 'organization_id', osmfp.org_name, osmfp.academic_year, osmfp.semester, COALESCE(SUM(osmfp.amount_paid),0)  total_amount_paid, osmfp.total_due 
        FROM (
            SELECT *
            FROM (
                SELECT *
                FROM (
                    SELECT DISTINCT organization_id as `org_id`, name as 'org_name', member_id as 'mem_id', full_name FROM (
                        SELECT *
                        FROM (SELECT * FROM ORGANIZATION) o
                        LEFT JOIN (SELECT organization_id as org_id, member_id as 'mem_id' FROM SERVES) s
                        ON o.organization_id=s.org_id
                    ) os
                    LEFT JOIN (SELECT member_id, username, name as 'full_name', password, batch, status, gender, is_admin FROM MEMBER) m
                    ON os.mem_id=m.member_id
                ) osm   
                LEFT JOIN  (
                    SELECT * 
                    FROM FINANCIAL_OBLIGATION
                ) fp
                ON osm.org_id=fp.organization_id
            ) r
            LEFT JOIN (
                SELECT payment_id, amount_paid, payment_date, record_id as 'p_record_id', member_id FROM PAYMENT
            ) p
            ON p.member_id = r.mem_id
        ) osmfp 
        GROUP BY member_id, record_id, organization_id 
        HAVING total_amount_paid < total_due AND osmfp.mem_id = {member_id};
    """)
    
    rows = db.cursor.fetchall()

    headers = ["Organization", "Obligation", "Academic Year", "Semester", "Amount Paid", "Total Due"]
    table_data = []

    for row in rows:
        obligation_name = row[3]
        organization_name = row[5]
        academic_year = row[6]
        semester = row[7]
        total_amount_paid = row[8]
        total_due = row[9]

        table_data.append([
            organization_name, obligation_name, academic_year, semester, total_amount_paid, total_due
        ])

    if table_data:
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    else:
        print("You have no outstanding dues!")


@screen
def pay_due():
    print("PAY DUE")
    member_id = member.member_id

    db.cursor.execute(f"""
        SELECT osmfp.record_id, osmfp.name as 'obligation_name', osmfp.org_name, osmfp.academic_year, osmfp.semester,
               COALESCE(SUM(osmfp.amount_paid), 0) as total_amount_paid, osmfp.total_due
        FROM (
            SELECT *
            FROM (
                SELECT *
                FROM (
                    SELECT DISTINCT organization_id as org_id, name as org_name, member_id as mem_id, full_name
                    FROM (
                        SELECT *
                        FROM (SELECT * FROM ORGANIZATION) o
                        LEFT JOIN (SELECT organization_id as org_id, member_id as mem_id FROM SERVES) s
                        ON o.organization_id = s.org_id
                    ) os
                    LEFT JOIN (SELECT member_id, username, name as full_name, password, batch, status, gender, is_admin FROM MEMBER) m
                    ON os.mem_id = m.member_id
                ) osm
                LEFT JOIN (SELECT * FROM FINANCIAL_OBLIGATION) fp
                ON osm.org_id = fp.organization_id
            ) r
            LEFT JOIN (SELECT payment_id, amount_paid, payment_date, record_id as p_record_id, member_id FROM PAYMENT) p
            ON p.member_id = r.mem_id AND p.record_id = r.record_id
        ) osmfp
        WHERE osmfp.mem_id = {member_id}
        GROUP BY osmfp.record_id
        HAVING total_amount_paid < total_due;
    """)
    
    dues = db.cursor.fetchall()

    if not dues:
        print("You have no outstanding dues!")
        return

    headers = ["Index", "Organization", "Obligation", "Academic Year", "Semester", "Amount Paid", "Total Due"]
    table_data = []

    for idx, row in enumerate(dues):
        record_id, obligation_name, org_name, academic_year, semester, total_paid, total_due = row
        table_data.append([idx + 1, org_name, obligation_name, academic_year, semester, total_paid, total_due])

    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

    choice = input("Enter the index of the obligation you want to pay (0 to cancel): ")
    if not choice.isdigit() or int(choice) < 0 or int(choice) > len(dues):
        print("Invalid choice.")
        return
    
    if int(choice) == 0:
        return

    selected_due = dues[int(choice) - 1]
    record_id = selected_due[0]

    amount = input("Enter amount to pay: ")
    try:
        amount = float(amount)
        if amount <= 0:
            print("Amount must be greater than 0.")
            return
    except ValueError:
        print("Invalid amount.")
        return

    now = datetime.now().strftime('%Y-%m-%d')

    db.cursor.execute("""
        INSERT INTO PAYMENT (amount_paid, payment_date, record_id, member_id)
        VALUES (%s, %s, %s, %s)
    """, (amount, now, record_id, member_id))
    db.conn.commit()
    print("Payment successful!")
   


@screen
def view_payment_history():
    print("MY PAYMENT HISTORY")
    member_id = member.member_id

    db.cursor.execute(f"""
        SELECT osmfp.mem_id as 'member_id', osmfp.full_name, osmfp.record_id, osmfp.name as 'obligation_name', osmfp.org_id as 'organization_id', osmfp.org_name, osmfp.academic_year, osmfp.semester, COALESCE(SUM(osmfp.amount_paid),0)  total_amount_paid, osmfp.total_due 
        FROM (
            SELECT *
            FROM (
                SELECT *
                FROM (
                    SELECT DISTINCT organization_id as `org_id`, name as 'org_name', member_id as 'mem_id', full_name FROM (
                        SELECT *
                        FROM (SELECT * FROM ORGANIZATION) o
                        LEFT JOIN (SELECT organization_id as org_id, member_id as 'mem_id' FROM SERVES) s
                        ON o.organization_id=s.org_id
                    ) os
                    LEFT JOIN (SELECT member_id, username, name as 'full_name', password, batch, status, gender, is_admin FROM MEMBER) m
                    ON os.mem_id=m.member_id
                ) osm   
                LEFT JOIN  (
                    SELECT * 
                    FROM FINANCIAL_OBLIGATION
                ) fp
                ON osm.org_id=fp.organization_id
            ) r
            LEFT JOIN (
                SELECT payment_id, amount_paid, payment_date, record_id as 'p_record_id', member_id FROM PAYMENT
            ) p
            ON p.member_id = r.mem_id
        ) osmfp 
        GROUP BY member_id, record_id, organization_id
        HAVING osmfp.mem_id = {member_id}
        ORDER BY osmfp.academic_year;
    """)
    
    rows = db.cursor.fetchall()

    headers = ["Organization", "Obligation", "Academic Year", "Semester", "Amount Paid", "Total Due"]
    table_data = []

    for row in rows:
        obligation_name = row[3]
        organization_name = row[5]
        academic_year = row[6]
        semester = row[7]
        total_amount_paid = row[8]
        total_due = row[9]

        table_data.append([
            organization_name, obligation_name, academic_year, semester, total_amount_paid, total_due
        ])

    if table_data:
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    else:
        print("You have no outstanding dues!")
    # insert code here

