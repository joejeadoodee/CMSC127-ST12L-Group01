import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from src.decorators import screen
import src.mariadb_connector as db
from src import member, navigate

# We'll keep the function names the same

@screen
def view_dues():
    # Main window for Financial Obligations
    root = tk.Tk()
    root.title("Financial Obligations")
    root.geometry("350x200")

    def on_settle_dues():
        root.withdraw()
        view_all_dues()
        root.deiconify()

    def on_view_payment_history():
        root.withdraw()
        view_payment_history()
        root.deiconify()

    def on_back():
        root.destroy()
        navigate.to_home('member')

    label = tk.Label(root, text="FINANCIAL OBLIGATIONS", font=("Arial", 14))
    label.pack(pady=10)

    btn1 = tk.Button(root, text="Settle Dues", width=25, command=on_settle_dues)
    btn1.pack(pady=5)

    btn2 = tk.Button(root, text="View Payment History", width=25, command=on_view_payment_history)
    btn2.pack(pady=5)

    btn0 = tk.Button(root, text="Back", width=25, command=on_back)
    btn0.pack(pady=5)

    root.mainloop()


@screen
def view_all_dues():
    # Fetch dues data first
    member_id = member.member_id
    username = member.username

    db.cursor.execute(f"""
        SELECT * FROM (
            SELECT s.member_id, m.username, o.name, f.record_id, f.name as `obligation_name`, f.semester, f.academic_year, f.total_due, f.due_date, 
            COALESCE(p.total_amount_paid, 0) as `total_amount_paid`
            FROM SERVES s
            LEFT JOIN MEMBER m ON s.member_id = m.member_id
            LEFT JOIN ORGANIZATION o ON o.organization_id = s.organization_id
            LEFT JOIN FINANCIAL_OBLIGATION f ON o.organization_id = f.organization_id
            LEFT JOIN (
                SELECT record_id, member_id, SUM(amount_paid) `total_amount_paid`
                FROM PAYMENT p
                GROUP BY record_id, member_id
            ) p ON f.record_id = p.record_id AND s.member_id = p.member_id
            WHERE s.member_id = {member_id}
            ORDER BY s.member_id, o.name, f.name
        ) result 
        WHERE total_amount_paid < total_due;
    """)

    rows = db.cursor.fetchall()

    # Setup the window
    window = tk.Toplevel()
    window.title("My Pending Dues")
    window.geometry("900x400")

    headers = ["Record id", "Organization", "Obligation", "Academic Year", "Semester", "Amount Paid", "Total Due"]
    tree = ttk.Treeview(window, columns=headers, show="headings")

    for h in headers:
        tree.heading(h, text=h)
        tree.column(h, width=120, anchor='center')

    # Populate table
    for row in rows:
        record_id = row[3]
        obligation_name = row[4]
        organization_name = row[2]
        academic_year = row[6]
        semester = row[5]
        total_amount_paid = row[9]
        total_due = row[7]
        tree.insert("", tk.END, values=(record_id, organization_name, obligation_name, academic_year, semester, total_amount_paid, total_due))

    tree.pack(expand=True, fill=tk.BOTH)

    def on_pay():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a row to pay.")
            return

        # Get values of the selected row
        values = tree.item(selected[0])['values']
        record_id = values[0]  # Record id is in first column

        try:
            amount_paid = simpledialog.askfloat("Payment", "Enter payment amount:", parent=window)
            if amount_paid is None:
                return

            payment_date = datetime.datetime.today().strftime('%Y-%m-%d')

            db.cursor.execute("""
                INSERT INTO PAYMENT(amount_paid, payment_date, record_id, member_id, username)
                VALUES (%s, %s, %s, %s, %s);
            """, (amount_paid, payment_date, record_id, member_id, username))
            db.conn.commit()

            messagebox.showinfo("Success", "✅ Payment recorded successfully.")
            window.destroy()  # Close and reopen to refresh data
            view_all_dues()

        except Exception as e:
            messagebox.showerror("Error", f"❌ Error processing payment: {e}")


    btn_pay = tk.Button(window, text="Pay Selected", command=on_pay)
    btn_pay.pack(pady=10)


@screen
def view_payment_history():
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

    window = tk.Toplevel()
    window.title("My Payment History")
    window.geometry("800x400")

    headers = ["Payment id", "Organization", "Obligation", "Amount Paid", "Payment date"]
    tree = ttk.Treeview(window, columns=headers, show="headings")

    for h in headers:
        tree.heading(h, text=h)
        tree.column(h, width=140, anchor='center')

    for row in rows:
        tree.insert("", tk.END, values=row)

    tree.pack(expand=True, fill=tk.BOTH)
