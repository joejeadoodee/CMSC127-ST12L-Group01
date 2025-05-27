from tkinter import messagebox, simpledialog
from tabulate import tabulate
from src.decorators import screen
import src.mariadb_connector as db
from src import organization, navigate
import tkinter as tk
from tkinter import ttk

import tkinter as tk
from tkinter import ttk

def view_reports():
    win = tk.Tk()
    win.title("View Reports")
    win.geometry("400x500")
    
    label = ttk.Label(win, text="VIEW REPORTS", font=("Arial", 16, "bold"))
    label.pack(pady=10)

    # Map option labels to their handler functions
    options = [
        ("Member Overview", member_overview),
        ("Unpaid Members", unpaid_members),
        ("Executive Committee", executive_committee),
        ("Historical Roles", historical_roles),
        ("Late Payments", late_payments),
        ("Member Status Analytics", member_status_analytics),
        ("Alumni Report", alumni_report),
        ("Financial Summary", financial_summary),
        ("Member with Highest Debt", member_with_highest_debt)
    ]

    # Create a button for each report
    for text, func in options:
        btn = ttk.Button(win, text=text, command=func)
        btn.pack(fill="x", padx=20, pady=5)

    # Back button to close this window and navigate home
    def back():
        win.destroy()
        navigate.to_home('organization')

    back_btn = ttk.Button(win, text="Back", command=back)
    back_btn.pack(pady=20, fill="x", padx=20)


@screen
def member_overview():
    win = tk.Toplevel()
    win.title("Member Overview")
    win.geometry("1000x400")

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
            MEMBER m ON m.member_id = s.member_id
        LEFT JOIN
            MEMBER_DEGREE_PROGRAM md ON m.member_id = md.member_id
        WHERE 
            s.organization_id = {organization_id}
        GROUP BY 
            m.member_id
    """

    db.cursor.execute(query)
    rows = db.cursor.fetchall()
    headers = ["Member ID", "Username", "Full Name", "Status", "Gender", "Degree Program", "Batch", "Role", "Committee"]

    tree = ttk.Treeview(win, columns=headers, show='headings')
    for header in headers:
        tree.heading(header, text=header)
        tree.column(header, width=120, anchor='center')

    for row in rows:
        tree.insert('', tk.END, values=row)

    tree.pack(expand=True, fill=tk.BOTH)
    ttk.Button(win, text="Close", command=win.destroy).pack(pady=10)


def unpaid_members():
    win = tk.Toplevel()
    win.title("Unpaid Members")
    win.geometry("1000x400")

    organization_id = organization.organization_id
    query = f"""
        SELECT r.organization_id, r.name, r.username, r.semester, r.academic_year, r.obligation_name, r.unpaid_amount, r.due_date  
        FROM (
            SELECT s.member_id, m.username, o.organization_id, o.name, f.record_id, f.name as obligation_name, f.semester, f.academic_year, f.total_due, f.due_date, 
                   COALESCE(p.total_amount_paid, 0) as total_amount_paid,
                   (f.total_due - COALESCE(p.total_amount_paid, 0)) AS unpaid_amount
            FROM SERVES s
            LEFT JOIN MEMBER m ON s.member_id = m.member_id
            LEFT JOIN ORGANIZATION o ON o.organization_id = s.organization_id
            LEFT JOIN FINANCIAL_OBLIGATION f ON o.organization_id = f.organization_id
            LEFT JOIN (
                SELECT record_id, member_id, SUM(amount_paid) AS total_amount_paid
                FROM PAYMENT
                GROUP BY record_id, member_id
            ) p ON f.record_id = p.record_id AND s.member_id = p.member_id
            WHERE f.record_id IS NOT NULL
              AND o.organization_id = {organization_id}
              AND (f.total_due - COALESCE(p.total_amount_paid, 0)) > 0
        ) r
        ORDER BY r.name, r.username, r.obligation_name, r.unpaid_amount DESC;
    """

    db.cursor.execute(query)
    rows = db.cursor.fetchall()
    headers = ["Organization Name", "Username", "Semester", "Academic Year", "Obligation", "Unpaid Amount", "Due Date"]
    processed_rows = [row[1:] for row in rows]

    tree = ttk.Treeview(win, columns=headers, show='headings')
    for header in headers:
        tree.heading(header, text=header)
        tree.column(header, width=140, anchor='center')

    for row in processed_rows:
        tree.insert('', tk.END, values=row)

    tree.pack(expand=True, fill=tk.BOTH)
    ttk.Button(win, text="Close", command=win.destroy).pack(pady=10)


def executive_committee():
    win = tk.Toplevel()
    win.title("Executive Committee")
    win.geometry("900x450")

    organization_id = organization.organization_id 

    # Input dialogs for school_year and semester
    school_year = simpledialog.askstring("Input", "Enter school year (e.g., 2024-2025):", parent=win)
    if not school_year:
        win.destroy()
        return
    semester = simpledialog.askstring("Input", "Enter semester (1st Semester/2nd Semester/Mid Semester):", parent=win)
    if not semester:
        win.destroy()
        return

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

    tree = ttk.Treeview(win, columns=headers, show='headings')
    for header in headers:
        tree.heading(header, text=header)
        tree.column(header, width=120, anchor='center')
    for row in rows:
        tree.insert('', tk.END, values=row)

    tree.pack(expand=True, fill=tk.BOTH)
    ttk.Button(win, text="Close", command=win.destroy).pack(pady=10)


def historical_roles():
    win = tk.Toplevel()
    win.title("Historical Roles")
    win.geometry("1100x500")

    organization_id = organization.organization_id
    role = simpledialog.askstring("Input", "Enter the role you want to view:", parent=win)
    if not role:
        win.destroy()
        return

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
            MEMBER m ON m.member_id = s.member_id
        LEFT JOIN
            MEMBER_DEGREE_PROGRAM md ON m.member_id = md.member_id
        WHERE 
            s.organization_id = {organization_id} AND
            s.role = '{role}'
        ORDER BY 
          s.school_year DESC,
          FIELD(s.semester, '1st semester', '2nd semester', 'Mid semester') DESC;
    """

    db.cursor.execute(query)
    rows = db.cursor.fetchall()

    headers = ["Member ID", "Username", "Full Name", "Status", "Gender", "Degree Program", "Batch", "Role", "Committee", "School Year", "Semester"]

    tree = ttk.Treeview(win, columns=headers, show='headings')
    for header in headers:
        tree.heading(header, text=header)
        tree.column(header, width=120, anchor='center')

    for row in rows:
        tree.insert('', tk.END, values=row)

    tree.pack(expand=True, fill=tk.BOTH)
    ttk.Button(win, text="Close", command=win.destroy).pack(pady=10)


def late_payments():
    win = tk.Toplevel()
    win.title("Late Payments")
    win.geometry("1000x450")

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
        LEFT JOIN FINANCIAL_OBLIGATION f ON f.record_id = p.record_id
        LEFT JOIN ORGANIZATION o ON f.organization_id = o.organization_id
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

    tree = ttk.Treeview(win, columns=headers, show='headings')
    for header in headers:
        tree.heading(header, text=header)
        tree.column(header, width=130, anchor='center')

    for row in rows:
        tree.insert('', tk.END, values=row)

    tree.pack(expand=True, fill=tk.BOTH)
    ttk.Button(win, text="Close", command=win.destroy).pack(pady=10)


def member_status_analytics():
    win = tk.Toplevel()
    win.title("Member Status Analytics")
    win.geometry("800x300")

    organization_id = organization.organization_id

    # Ask for number of semesters
    n = simpledialog.askinteger("Input", "Enter how many recent semesters to analyze (e.g., 5):", parent=win, minvalue=1)
    if n is None:
        win.destroy()
        return
    if n == 1:
        n = 2

    year_threshold_query = f"(YEAR(CURDATE()) - FLOOR({n} / 2))"

    query = f"""
        SELECT 
            s.organization_id,
            SUM(CASE WHEN m.status = 'Active' THEN 1 ELSE 0 END) AS active_members,
            SUM(CASE WHEN m.status = 'Inactive' OR m.status = 'Graduated' THEN 1 ELSE 0 END) AS inactive_members,
            COUNT(*) AS total_members,
            ROUND((SUM(CASE WHEN m.status = 'Active' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS active_percentage,
            ROUND((SUM(CASE WHEN m.status = 'Inactive' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS inactive_percentage
        FROM 
            MEMBER m
        JOIN 
            SERVES s ON m.member_id = s.member_id AND m.username = s.username
        WHERE 
            s.organization_id = {organization_id}
            AND CAST(LEFT(s.school_year, 4) AS UNSIGNED) >= {year_threshold_query}
            AND s.semester IN ('1st semester', '2nd semester', 'Mid semester')
        GROUP BY 
            s.organization_id;
    """

    db.cursor.execute(query)
    rows = db.cursor.fetchall()

    headers = ["Org ID", "Active", "Inactive", "Total", "Active %", "Inactive %"]

    if not rows:
        messagebox.showinfo("Info", "No data found for the given criteria.", parent=win)
        win.destroy()
        return

    tree = ttk.Treeview(win, columns=headers, show='headings')
    for header in headers:
        tree.heading(header, text=header)
        tree.column(header, width=100, anchor='center')

    for row in rows:
        tree.insert('', tk.END, values=row)

    tree.pack(expand=True, fill=tk.BOTH)
    ttk.Button(win, text="Close", command=win.destroy).pack(pady=10)


def alumni_report():
    win = tk.Toplevel()
    win.title("Alumni Report")
    win.geometry("1000x400")

    organization_id = organization.organization_id

    input_year = simpledialog.askstring("Input", "Enter graduation year (YYYY):", parent=win)
    if input_year is None:
        win.destroy()
        return
    if not input_year.isdigit() or len(input_year) != 4:
        messagebox.showerror("Error", "Invalid year entered. Aborting.", parent=win)
        win.destroy()
        return

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
            MEMBER m ON m.member_id = s.member_id
        LEFT JOIN
            MEMBER_DEGREE_PROGRAM md ON m.member_id = md.member_id
        WHERE 
            s.organization_id = {organization_id}
            AND m.graduation_date IS NOT NULL
            AND YEAR(m.graduation_date) = {input_year}
        GROUP BY 
            m.member_id
    """

    db.cursor.execute(query)
    rows = db.cursor.fetchall()

    headers = ["Member ID", "Username", "Full Name", "Status", "Gender",
               "Degree Program", "Batch", "Role", "Committee"]

    tree = ttk.Treeview(win, columns=headers, show='headings')
    for header in headers:
        tree.heading(header, text=header)
        tree.column(header, width=110, anchor='center')

    for row in rows:
        tree.insert('', tk.END, values=row)

    tree.pack(expand=True, fill=tk.BOTH)
    ttk.Button(win, text="Close", command=win.destroy).pack(pady=10)


def financial_summary():
    win = tk.Toplevel()
    win.title("Financial Summary")
    win.geometry("500x200")

    organization_id = organization.organization_id

    try:
        input_year = simpledialog.askinteger("Input", "Enter cutoff year (YYYY):", parent=win, minvalue=1900, maxvalue=2100)
        if input_year is None:
            win.destroy()
            return
    except Exception:
        messagebox.showerror("Error", "Invalid year entered. Aborting.", parent=win)
        win.destroy()
        return

    query = f"""
        SELECT 
            SUM(sub.total_amount_paid) AS total_paid,
            SUM(sub.total_due - sub.total_amount_paid) AS total_unpaid
        FROM (
            SELECT 
                s.member_id, 
                m.username, 
                o.name AS organization_name, 
                f.record_id, 
                f.name AS obligation_name, 
                f.semester, 
                f.academic_year, 
                f.total_due, 
                f.due_date, 
                COALESCE(p.total_amount_paid, 0) AS total_amount_paid
            FROM SERVES s
            LEFT JOIN MEMBER m ON s.member_id = m.member_id
            LEFT JOIN ORGANIZATION o ON o.organization_id = s.organization_id
            LEFT JOIN FINANCIAL_OBLIGATION f ON o.organization_id = f.organization_id
            LEFT JOIN (
                SELECT record_id, member_id, SUM(amount_paid) AS total_amount_paid
                FROM PAYMENT
                GROUP BY record_id, member_id
            ) p ON f.record_id = p.record_id AND s.member_id = p.member_id
            WHERE f.record_id IS NOT NULL
              AND o.organization_id = {organization_id}
              AND YEAR(f.due_date) = {input_year}
        ) AS sub;
    """

    db.cursor.execute(query)
    result = db.cursor.fetchone()

    if result:
        total_paid = result[0] if result[0] is not None else 0.0
        total_unpaid = result[1] if result[1] is not None else 0.0
        label_text = (f"As of the end of {input_year}:\n\n"
                      f"Total Paid:   ₱ {total_paid:,.2f}\n"
                      f"Total Unpaid: ₱ {total_unpaid:,.2f}")
    else:
        label_text = "No financial data found."

    label = ttk.Label(win, text=label_text, justify="center", font=("Segoe UI", 12))
    label.pack(expand=True, fill=tk.BOTH, padx=20, pady=40)
    ttk.Button(win, text="Close", command=win.destroy).pack(pady=10)


def member_with_highest_debt():
    win = tk.Toplevel()
    win.title("Members with Highest Unpaid Obligations")
    win.geometry("600x300")

    organization_id = organization.organization_id
    semester = simpledialog.askstring("Input", "Enter Semester (e.g., '1st Semester'):", parent=win)
    if not semester:
        win.destroy()
        return
    academic_year = simpledialog.askstring("Input", "Enter academic year (e.g., '2025'):", parent=win)
    if not academic_year:
        win.destroy()
        return

    query = f"""
        SELECT DISTINCT r.username, r.obligation_name, r.unpaid_amount FROM (
            SELECT s.member_id, m.username, o.organization_id, o.name, f.record_id, f.name as obligation_name, f.semester, f.academic_year, f.total_due, f.due_date, 
                   COALESCE(p.total_amount_paid, 0) as total_amount_paid,
                   (f.total_due - COALESCE(p.total_amount_paid, 0)) AS unpaid_amount
            FROM SERVES s
            LEFT JOIN MEMBER m ON s.member_id = m.member_id
            LEFT JOIN ORGANIZATION o ON o.organization_id = s.organization_id
            LEFT JOIN FINANCIAL_OBLIGATION f ON o.organization_id = f.organization_id
            LEFT JOIN (
                SELECT record_id, member_id, SUM(amount_paid) AS total_amount_paid
                FROM PAYMENT
                GROUP BY record_id, member_id
            ) p ON f.record_id = p.record_id AND s.member_id = p.member_id
            WHERE f.record_id IS NOT NULL 
              AND o.organization_id = {organization_id}
              AND (f.total_due - COALESCE(p.total_amount_paid, 0)) > 0
              AND f.semester = '{semester}' 
              AND f.academic_year = {academic_year}
        ) r
        ORDER BY r.username, r.unpaid_amount DESC;
    """

    try:
        db.cursor.execute(query)
        rows = db.cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Database Error", f"Error fetching data: {e}", parent=win)
        win.destroy()
        return

    if not rows:
        messagebox.showinfo("Info", "No members have unpaid obligations for that semester and academic year.", parent=win)
        win.destroy()
        return

    headers = ["Username", "Obligation", "Unpaid Amount (₱)"]
    tree = ttk.Treeview(win, columns=headers, show="headings")
    for header in headers:
        tree.heading(header, text=header)
        tree.column(header, width=200, anchor="center")

    for row in rows:
        tree.insert("", tk.END, values=(row[0], row[1], f"{row[2]:,.2f}"))

    tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    ttk.Button(win, text="Close", command=win.destroy).pack(pady=5)
