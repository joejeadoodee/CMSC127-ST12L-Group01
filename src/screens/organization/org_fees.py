import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from src.decorators import screen
import src.mariadb_connector as db
from src import organization, navigate
import datetime


@screen
def manage_fees():
    root = tk.Tk()
    root.title("Manage Fees")
    root.geometry("350x300")

    def on_add_fee():
        root.withdraw()
        add_membership_fee()
        root.deiconify()

    def on_update_fee():
        root.withdraw()
        update_membership_fee()
        root.deiconify()

    def on_delete_fee():
        root.withdraw()
        delete_membership_fee()
        root.deiconify()

    def on_view_fees():
        root.withdraw()
        view_fee_records()
        root.deiconify()

    def on_back():
        root.destroy()
        navigate.to_home('organization')

    label = tk.Label(root, text="MANAGE FEES", font=("Arial", 16))
    label.pack(pady=15)

    btn_add = tk.Button(root, text="Add Membership Fee", width=25, command=on_add_fee)
    btn_add.pack(pady=5)

    btn_update = tk.Button(root, text="Update Membership Fee", width=25, command=on_update_fee)
    btn_update.pack(pady=5)

    btn_delete = tk.Button(root, text="Delete Membership Fee", width=25, command=on_delete_fee)
    btn_delete.pack(pady=5)

    btn_view = tk.Button(root, text="View Fee Records", width=25, command=on_view_fees)
    btn_view.pack(pady=5)


    btn_back = tk.Button(root, text="Back", width=25, command=on_back)
    btn_back.pack(pady=10)

    root.mainloop()


@screen
def add_membership_fee():
    window = tk.Toplevel()
    window.title("Add Membership Fee")
    window.geometry("400x350")

    tk.Label(window, text="Fee Name:").pack(pady=5)
    name_entry = tk.Entry(window, width=30)
    name_entry.pack()

    tk.Label(window, text="Semester:").pack(pady=5)
    semester_entry = tk.Entry(window, width=30)
    semester_entry.pack()

    tk.Label(window, text="Academic Year:").pack(pady=5)
    academic_year_entry = tk.Entry(window, width=30)
    academic_year_entry.pack()

    tk.Label(window, text="Total Due Amount:").pack(pady=5)
    total_due_entry = tk.Entry(window, width=30)
    total_due_entry.pack()

    tk.Label(window, text="Due Date (YYYY-MM-DD):").pack(pady=5)
    due_date_entry = tk.Entry(window, width=30)
    due_date_entry.pack()

    def on_submit():
        name = name_entry.get().strip()
        semester = semester_entry.get().strip()
        academic_year = academic_year_entry.get().strip()
        total_due = total_due_entry.get().strip()
        due_date = due_date_entry.get().strip()

        if not all([name, semester, academic_year, total_due, due_date]):
            messagebox.showwarning("Missing Data", "Please fill in all fields.")
            return

        try:
            total_due_int = int(total_due)
        except ValueError:
            messagebox.showerror("Invalid Input", "Total due must be a number.")
            return

        # Basic date validation
        try:
            datetime.datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Input", "Due date must be in YYYY-MM-DD format.")
            return

        try:
            db.cursor.execute(
                "INSERT INTO FINANCIAL_OBLIGATION (name, semester, academic_year, total_due, due_date, organization_id) VALUES (%s, %s, %s, %s, %s, %s)",
                (name, semester, academic_year, total_due_int, due_date, organization.organization_id)
            )
            db.conn.commit()
            messagebox.showinfo("Success", "Fee added successfully.")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to add fee: {e}")

    submit_btn = tk.Button(window, text="Add Fee", command=on_submit)
    submit_btn.pack(pady=20)


@screen
def update_membership_fee():
    window = tk.Toplevel()
    window.title("Update Membership Fee")
    window.geometry("350x250")

    tk.Label(window, text="Fee ID to update:").pack(pady=5)
    fee_id_entry = tk.Entry(window, width=30)
    fee_id_entry.pack()

    tk.Label(window, text="New Total Due Amount:").pack(pady=5)
    new_amount_entry = tk.Entry(window, width=30)
    new_amount_entry.pack()

    def on_update():
        fee_id = fee_id_entry.get().strip()
        new_amount = new_amount_entry.get().strip()

        if not fee_id or not new_amount:
            messagebox.showwarning("Missing Data", "Please fill in all fields.")
            return

        if not fee_id.isdigit():
            messagebox.showerror("Invalid Input", "Fee ID must be numeric.")
            return

        try:
            new_amount_int = int(new_amount)
        except ValueError:
            messagebox.showerror("Invalid Input", "Total due amount must be a number.")
            return

        try:
            db.cursor.execute(
                "UPDATE FINANCIAL_OBLIGATION SET total_due = %s WHERE record_id = %s",
                (new_amount_int, fee_id)
            )
            if db.cursor.rowcount > 0:
                db.conn.commit()
                messagebox.showinfo("Success", "Fee updated successfully.")
                window.destroy()
            else:
                messagebox.showwarning("Not Found", "No fee found with the provided Fee ID.")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update fee: {e}")

    update_btn = tk.Button(window, text="Update Fee", command=on_update)
    update_btn.pack(pady=20)


@screen
def delete_membership_fee():
    window = tk.Toplevel()
    window.title("Delete Membership Fee")
    window.geometry("300x180")

    tk.Label(window, text="Fee ID to delete:").pack(pady=5)
    fee_id_entry = tk.Entry(window, width=30)
    fee_id_entry.pack()

    def on_delete():
        fee_id = fee_id_entry.get().strip()

        if not fee_id:
            messagebox.showwarning("Missing Data", "Please enter Fee ID.")
            return

        if not fee_id.isdigit():
            messagebox.showerror("Invalid Input", "Fee ID must be numeric.")
            return

        try:
            db.cursor.execute(
                "DELETE FROM FINANCIAL_OBLIGATION WHERE record_id = %s",
                (fee_id,)
            )
            if db.cursor.rowcount > 0:
                db.conn.commit()
                messagebox.showinfo("Success", "Fee deleted successfully.")
                window.destroy()
            else:
                messagebox.showwarning("Not Found", "No fee found with the provided Fee ID.")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to delete fee: {e}")

    delete_btn = tk.Button(window, text="Delete Fee", command=on_delete)
    delete_btn.pack(pady=20)

def view_fee_records():
    window = tk.Toplevel()
    window.title("Fee Records")
    window.geometry("1000x400")

    columns = ["ID", "Semester", "Academic Year", "Name", "Total Due", "Due Date"]
    tree = ttk.Treeview(window, columns=columns, show='headings', selectmode='browse')

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

    tree.pack(expand=True, fill=tk.BOTH)

    def show_payments():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a record first.")
            return

        record_id = tree.item(selected[0])["values"][0]
        open_payment_window(record_id)

    show_button = ttk.Button(window, text="Show Payments", command=show_payments)
    show_button.pack(pady=10)

    try:
        db.cursor.execute("SELECT record_id, semester, academic_year, name, total_due, due_date FROM FINANCIAL_OBLIGATION")
        records = db.cursor.fetchall()
        for rec in records:
            due_date_str = str(rec[5]) if rec[5] else ""
            tree.insert("", tk.END, values=(rec[0], rec[1], rec[2], rec[3], rec[4], due_date_str))
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to retrieve fee records: {e}")


def open_payment_window(record_id):
    payment_window = tk.Toplevel()
    payment_window.title(f"Payments for Record ID {record_id}")
    payment_window.geometry("800x300")

    columns = ["Payment ID", "Username", "Total Paid", "Payment Date"]
    tree = ttk.Treeview(payment_window, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

    tree.pack(expand=True, fill=tk.BOTH)

    try:
        query = """
        SELECT 
            p.payment_id, 
            m.username,
            SUM(p.amount_paid), 
            p.payment_date
        FROM PAYMENT p 
        LEFT JOIN FINANCIAL_OBLIGATION f ON f.record_id = p.record_id
        LEFT JOIN ORGANIZATION o ON f.organization_id = o.organization_id
        LEFT JOIN MEMBER m ON m.member_id = p.member_id
        WHERE f.record_id = %s
        GROUP BY m.username
        ORDER BY p.member_id, o.name, f.name, p.payment_date DESC
        """
        db.cursor.execute(query, (record_id,))
        rows = db.cursor.fetchall()

        for row in rows:
            tree.insert("", tk.END, values=row)

    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to retrieve payment records: {e}")
