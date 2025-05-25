from tabulate import tabulate
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
    organization_id = organization.organization_id
    query = f"""
       SELECT 
        m.member_id,
        m.username,
        m.name,
        m.status,
        m.gender,
        md.degree_program,
        m.batch,
        s.role,
        s.committee
        FROM 
            SERVES s
        LEFT JOIN 
            MEMBER m
        ON m.member_id = s.member_id
        LEFT JOIN
            MEMBER_DEGREE_PROGRAM md
        ON m.member_id = md.member_id
        WHERE 
            s.organization_id = {organization_id}
    """

    db.cursor.execute(query)

    rows = db.cursor.fetchall()

    headers = ["Member id", "Username", "Full Name", "Status", "Gender", "Degree Program", "Batch", "Role", "Committee"]        

    table_str = tabulate(rows, headers=headers, tablefmt="fancy_grid")
    indented_table = "\n".join([f"      {line}" for line in table_str.splitlines()])
    print(indented_table)
    input("Press Enter to return...")

@screen
def unpaid_members():
    print("UNPAID MEMBERS")
    organization_id = organization.organization_id
    query = f"""
       SELECT r.organization_id, r.name, r.username, r.semester, r.academic_year, r.obligation_name, r.unpaid_amount, r.due_date  
       FROM (
            SELECT s.member_id, m.username, o.organization_id, o.name, f.record_id, f.name as `obligation_name`, f.semester, f.academic_year, f.total_due, f.due_date, 
            COALESCE(p.total_amount_paid, 0) as `total_amount_paid`,
            (f.total_due - COALESCE(p.total_amount_paid, 0)) AS `unpaid_amount`
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
            WHERE f.record_id IS NOT NULL AND o.organization_id = {organization_id} AND (f.total_due - COALESCE(p.total_amount_paid, 0)) > 0
            ORDER BY s.member_id, o.name, f.name
        ) r
        ORDER BY r.name, r.username, r.obligation_name, `unpaid_amount` DESC;
    """

    db.cursor.execute(query)

    rows = db.cursor.fetchall()
    result = []
    for row in rows:
        result.append(row[2:])

    headers = ["Username", "Semester", "Academic Year", "Obligation title", "Unpaid amount", "Due date"]        

    table_str = tabulate(result, headers=headers, tablefmt="fancy_grid")
    indented_table = "\n".join([f"      {line}" for line in table_str.splitlines()])
    print(indented_table)
    input("Press Enter to return...")

@screen
def executive_committee():
    print("EXECUTIVE COMMITTEE")

    organization_id = organization.organization_id 
    school_year = input("Enter school year (e.g., 2024-2025): ")
    semester = input("Enter semester (1st Semester/2nd Semester/Mid Semester): ")

    query = f"""
        SELECT 
            m.member_id,
            m.username,
            m.name,
            s.role,
            s.semester,
            s.committee,
            s.school_year,
            s.organization_id
        FROM 
            MEMBER m
        JOIN 
            SERVES s ON m.member_id = s.member_id AND m.username = s.username
        WHERE 
            s.organization_id = {organization_id} AND
            s.semester = '{semester}' AND
            s.school_year = '{school_year}' AND
            s.role != 'Member';
    """

    db.cursor.execute(query)
    rows = db.cursor.fetchall()

    headers = ["Member ID", "Username", "Name", "Role", "Committee", "School Year", "Organization ID"]
    table_str = tabulate(rows, headers=headers, tablefmt="fancy_grid")
    indented_table = "\n".join([f"      {line}" for line in table_str.splitlines()])
    print(indented_table)

    input("Press Enter to return...")


@screen
def historical_roles():
    print("HISTORICAL ROLES")
    organization_id = organization.organization_id
    role = input("Enter the role you want to view: ")
    query = f"""
       SELECT 
        m.member_id,
        m.username,
        m.name,
        m.status,
        m.gender,
        md.degree_program,
        m.batch,
        s.role,
        s.committee,
        s.school_year,
        s.semester
        FROM 
            SERVES s
        LEFT JOIN 
            MEMBER m
        ON m.member_id = s.member_id
        LEFT JOIN
            MEMBER_DEGREE_PROGRAM md
        ON m.member_id = md.member_id
        WHERE 
            s.organization_id = {organization_id} AND
            s.role = '{role}'
        ORDER BY 
          s.school_year DESC,
          FIELD(s.semester, '1st semester', '2nd semester', 'Mid semester') DESC;
    """

    db.cursor.execute(query)

    rows = db.cursor.fetchall()

    headers = ["Member id", "Username", "Full Name", "Status", "Gender", "Degree Program", "Batch", "Role", "Committee", "School Year", "Semester"]        

    table_str = tabulate(rows, headers=headers, tablefmt="fancy_grid")
    indented_table = "\n".join([f"      {line}" for line in table_str.splitlines()])
    print(indented_table)
    input("Press Enter to return...")


@screen
def late_payments():
    print("LATE PAYMENTS")
    organization_id = organization.organization_id
    query = f"""
        SELECT 
            p.payment_id, 
            o.name AS organization_name, 
            f.name AS obligation_name, 
            p.amount_paid, 
            p.payment_date, 
            p.member_id, 
            f.due_date
        FROM PAYMENT p 
        LEFT JOIN FINANCIAL_OBLIGATION f
            ON f.record_id = p.record_id
        LEFT JOIN ORGANIZATION o
            ON f.organization_id = o.organization_id
        WHERE 
            p.payment_date > f.due_date AND o.organization_id={organization_id}
        ORDER BY 
            p.member_id, 
            o.name, 
            f.name, 
            p.payment_date DESC;
    """

    db.cursor.execute(query)
    rows = db.cursor.fetchall()

    headers = [
        "Payment ID", 
        "Organization", 
        "Obligation", 
        "Amount Paid", 
        "Payment Date", 
        "Member ID", 
        "Due Date"
    ]        

    table_str = tabulate(rows, headers=headers, tablefmt="fancy_grid")
    indented_table = "\n".join([f"      {line}" for line in table_str.splitlines()])
    print(indented_table)
    input("Press Enter to return...")


@screen
def member_status_analytics():
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
