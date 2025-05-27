import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tabulate import tabulate
from src.decorators import screen
import src.mariadb_connector as db
from src import organization, navigate

@screen
def manage_members():
    root = tk.Tk()
    root.title("Manage Members")
    root.geometry("400x350")

    def on_view_members():
        root.withdraw()
        view_members()
        root.deiconify()

    def on_add_member():
        root.withdraw()
        add_member()
        root.deiconify()

    def on_update_member_role_status():
        root.withdraw()
        update_member_role_status()
        root.deiconify()

    def on_search_members():
        root.withdraw()
        search_members()
        root.deiconify()

    def on_delete_member():
        root.withdraw()
        delete_member()
        root.deiconify()

    def on_back():
        root.destroy()
        navigate.to_home('organization')

    tk.Label(root, text="MANAGE MEMBERS", font=("Arial", 16)).pack(pady=15)

    tk.Button(root, text="View All Members", width=30, command=on_view_members).pack(pady=5)
    tk.Button(root, text="Add Member", width=30, command=on_add_member).pack(pady=5)
    tk.Button(root, text="Update Member Role/Status", width=30, command=on_update_member_role_status).pack(pady=5)
    tk.Button(root, text="Search Members", width=30, command=on_search_members).pack(pady=5)
    tk.Button(root, text="Delete Member", width=30, command=on_delete_member).pack(pady=5)
    tk.Button(root, text="Back", width=30, command=on_back).pack(pady=15)

    root.mainloop()

@screen
def add_member():
    window = tk.Toplevel()
    window.title("Add New Member")
    window.geometry("350x350")

    labels = [
        "Member ID:",
        "Role (President/Member/Others):",
        "Semester:",
        "School Year:",
        "Committee:",
    ]
    entries = []

    for label_text in labels:
        tk.Label(window, text=label_text).pack(pady=5)

        if label_text == "Semester:":
            semester_combo = ttk.Combobox(window, values=["1st semester", "2nd semester", "Mid semester"], state="readonly", width=27)
            semester_combo.pack()
            entries.append(semester_combo)
        else:
            entry = tk.Entry(window, width=30)
            entry.pack()
            entries.append(entry)

    def on_submit():
        member_id = entries[0].get().strip()
        role = entries[1].get().strip()
        semester = entries[2].get().strip()
        school_year = entries[3].get().strip()
        committee = entries[4].get().strip()

        if not all([member_id, role, semester, school_year]):
            messagebox.showwarning("Invalid Input", "All fields except committee are required.")
            return

        try:
            print(member_id)
            db.cursor.execute("SELECT username FROM MEMBER WHERE member_id = %s", (member_id,))
            result = db.cursor.fetchone()

            if result:
                username = result[0]
                db.cursor.execute("""
                    INSERT INTO SERVES (member_id, username, organization_id, role, school_year, committee, semester)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (member_id, username, organization.organization_id, role, school_year, committee or None, semester))

                db.conn.commit()
                messagebox.showinfo("Success", "Member added successfully.")
                window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error while adding member: {e}")

    tk.Button(window, text="Submit", command=on_submit).pack(pady=20)



@screen
def update_member_role_status():
    window = tk.Toplevel()
    window.title("Update Member Role/Status")
    window.geometry("350x400")

    labels = [
        "Member ID:",
        "Role (President/Member/Others):",
        "Semester:",
        "School Year:",
        "Committee:",
        "New status:"
    ]
    entries = []

    for label_text in labels:
        tk.Label(window, text=label_text).pack(pady=5)

        if label_text == "Semester:":
            semester_combo = ttk.Combobox(window, values=["1st semester", "2nd semester", "Mid semester"], state="readonly", width=27)
            semester_combo.pack()
            entries.append(semester_combo)
        else:
            entry = tk.Entry(window, width=30)
            entry.pack()
            entries.append(entry)

    def on_submit():
        try:
            member_id = int(entries[0].get().strip())  # Convert input to int
        except ValueError:
            messagebox.showerror("Invalid Input", "Member ID must be a number.")
            return

        role = entries[1].get().strip()
        semester = entries[2].get().strip()
        school_year = entries[3].get().strip()
        committee = entries[4].get().strip()
        status = entries[5].get().strip()

        if not all([member_id, role, semester, school_year, status]):
            messagebox.showwarning("Invalid Input", "All fields except committee are required.")
            return

        try:
            db.cursor.execute("SELECT username FROM MEMBER WHERE member_id = %s", (member_id,))
            result = db.cursor.fetchone()

            if result:
                username = result[0]
                db.cursor.execute("""
                    INSERT INTO SERVES (member_id, username, organization_id, role, school_year, committee, semester)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (member_id, username, organization.organization_id, role, school_year, committee or None, semester))
                # Update MEMBER status
                db.cursor.execute("""
                    UPDATE MEMBER SET status = %s WHERE member_id = %s
                """, (status, member_id))

                db.conn.commit()
                messagebox.showinfo("Success", "Member updated successfully.")
                window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error while adding member: {e}")

    tk.Button(window, text="Submit", command=on_submit).pack(pady=20)



@screen
def delete_member():
    window = tk.Toplevel()
    window.title("Delete Member")
    window.geometry("300x180")

    tk.Label(window, text="Member ID to delete:").pack(pady=5)
    member_id_entry = tk.Entry(window, width=30)
    member_id_entry.pack()

    def on_delete():
        member_id = member_id_entry.get().strip()

        if not member_id:
            messagebox.showwarning("Missing Data", "Please enter Member ID.")
            return

        if messagebox.askyesno("Confirm Deletion", f"Delete member {member_id}?"):
            try:
                db.cursor.execute("DELETE FROM SERVES WHERE member_id = %s", (member_id,))
                if db.cursor.rowcount == 0:
                    messagebox.showinfo("Not Found", "No member found with that ID.")
                else:
                    db.conn.commit()
                    messagebox.showinfo("Success", "Member deleted successfully.")
                    window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while deleting the member: {e}")

    tk.Button(window, text="Delete Member", command=on_delete).pack(pady=20)

@screen
def search_members():
    window = tk.Toplevel()
    window.title("Search Members")
    window.geometry("600x400")

    tk.Label(window, text="Enter name, ID, or keyword:").pack(pady=5)
    query_entry = tk.Entry(window, width=50)
    query_entry.pack(pady=5)

    tree_columns = ["Member ID", "Name", "Username", "Status"]
    tree = ttk.Treeview(window, columns=tree_columns, show="headings")
    for col in tree_columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(expand=True, fill=tk.BOTH, pady=10)

    def on_search():
        query = query_entry.get().strip()
        if not query:
            messagebox.showwarning("Missing Data", "Please enter a search keyword.")
            return
        try:
            search_query = f"%{query}%"
            
            try:
                member_id_int = int(query)
            except ValueError:
                member_id_int = None

            if member_id_int is not None:
                db.cursor.execute("""
                    SELECT member_id, name, username, status 
                    FROM MEMBER 
                    WHERE name LIKE %s OR username LIKE %s OR member_id = %s
                """, (search_query, search_query, member_id_int))
            else:
                db.cursor.execute("""
                    SELECT member_id, name, username, status 
                    FROM MEMBER 
                    WHERE name LIKE %s OR username LIKE %s
                """, (search_query, search_query))

            results = db.cursor.fetchall()

            for i in tree.get_children():
                tree.delete(i)

            if not results:
                messagebox.showinfo("No Results", "No matching members found.")
            else:
                for member in results:
                    tree.insert("", tk.END, values=member)
        except Exception as e:
            messagebox.showerror("Error", f"Error while searching members: {e}")


    tk.Button(window, text="Search", command=on_search).pack(pady=10)

@screen
def update_member_role_status():
    window = tk.Toplevel()
    window.title("Update Member Role/Status")
    window.geometry("350x250")

    tk.Label(window, text="Member ID:").pack(pady=5)
    member_id_entry = tk.Entry(window, width=30)
    member_id_entry.pack()

    tk.Label(window, text="New Role:").pack(pady=5)
    role_entry = tk.Entry(window, width=30)
    role_entry.pack()

    tk.Label(window, text="New Status:").pack(pady=5)
    status_entry = tk.Entry(window, width=30)
    status_entry.pack()

    def on_update():
        member_id = member_id_entry.get().strip()
        role = role_entry.get().strip()
        status = status_entry.get().strip()

        if not member_id or not role or not status:
            messagebox.showwarning("Missing Data", "Please fill in all fields.")
            return

        try:
            db.cursor.execute("""
                UPDATE SERVES SET role = %s WHERE member_id = %s
            """, (role, member_id))

            db.cursor.execute("""
                UPDATE MEMBER SET status = %s WHERE member_id = %s
            """, (status, member_id))

            if db.cursor.rowcount == 0:
                messagebox.showinfo("Not Found", "No member found with that ID.")
            else:
                db.conn.commit()
                messagebox.showinfo("Success", "Member role/status updated successfully.")
                window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error while updating member role/status: {e}")

    tk.Button(window, text="Update", command=on_update).pack(pady=20)

@screen
def view_members():
    window = tk.Toplevel()
    window.title("View Members")
    window.geometry("1200x400")

    columns = ["Member ID", "Username", "Full Name", "Status", "Gender", "Degree Program", "Batch", "Role", "Committee"]
    tree = ttk.Treeview(window, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

    tree.pack(expand=True, fill=tk.BOTH)

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
            s.organization_id = %s
        GROUP BY
            s.member_id
    """

    try:
        db.cursor.execute(query, (organization_id,))
        rows = db.cursor.fetchall()

        for rec in rows:
            tree.insert("", tk.END, values=rec)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve members: {e}")
