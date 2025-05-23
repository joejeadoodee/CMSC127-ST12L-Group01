import tkinter as tk
from tkinter import messagebox
from tkinter import font

from src.decorators import screen
from src import navigate
import src.mariadb_connector as db
from src.utils import center_window


# ------------------ Sign up as a Member ------------------

@screen
def sign_up_member():
    win = tk.Tk()
    win.title("Sign Up as Member")
    win.geometry("400x450")
    center_window(win, 400, 450)

    heading_font = font.Font(family='Georgia', size=16, weight='bold')
    label_font = font.Font(family='Arial', size=12)

    def submit():
        name = name_entry.get()
        username = username_entry.get()
        batch = batch_entry.get()
        gender = gender_entry.get()
        password = password_entry.get()
        repassword = repassword_entry.get()

        if password != repassword:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        try:
            insert_query = f"""
                INSERT INTO MEMBER (username, name, password, batch, status, gender, is_admin)
                VALUES ('{username}', '{name}', '{password}', {int(batch)}, 'Active', '{gender}', FALSE)
            """
            db.cursor.execute(insert_query)
            messagebox.showinfo("Success", "Signed up successfully!")
            win.destroy()
            navigate.to_welcome()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    tk.Label(win, text="Sign Up as Member", font=heading_font).pack(pady=10)

    fields = [
        ("Full Name", "name_entry"),
        ("Username", "username_entry"),
        ("Batch Year", "batch_entry"),
        ("Gender", "gender_entry"),
        ("Password", "password_entry"),
        ("Retype Password", "repassword_entry"),
    ]
    
    entries = {}
    for label, var_name in fields:
        tk.Label(win, text=label, font=label_font).pack(pady=(5, 0))
        entry = tk.Entry(win, show="*" if "password" in var_name else None)
        entry.pack()
        entries[var_name] = entry

    name_entry = entries["name_entry"]
    username_entry = entries["username_entry"]
    batch_entry = entries["batch_entry"]
    gender_entry = entries["gender_entry"]
    password_entry = entries["password_entry"]
    repassword_entry = entries["repassword_entry"]

    tk.Button(win, text="Sign Up", command=submit, width=20).pack(pady=20)
    tk.Button(win, text="Back", command=lambda: [win.destroy(), navigate.to_welcome()]).pack()

    win.mainloop()


# ------------------ Sign up as an Organization ------------------

@screen
def sign_up_org():
    win = tk.Tk()
    win.title("Sign Up as Organization")
    win.geometry("400x400")
    center_window(win, 400, 400)

    heading_font = font.Font(family='Georgia', size=16, weight='bold')
    label_font = font.Font(family='Arial', size=12)

    def submit():
        org_name = name_entry.get()
        password = password_entry.get()
        repassword = repassword_entry.get()

        if password != repassword:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        try:
            insert_query = f"""
                INSERT INTO ORGANIZATION (name, password, number_of_members)
                VALUES ('{org_name}', '{password}', 0)
            """
            db.cursor.execute(insert_query)
            messagebox.showinfo("Success", "Signed up successfully!")
            win.destroy()
            navigate.to_welcome()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    tk.Label(win, text="Sign Up as Organization", font=heading_font).pack(pady=10)

    tk.Label(win, text="Organization Name", font=label_font).pack()
    name_entry = tk.Entry(win)
    name_entry.pack()

    tk.Label(win, text="Password", font=label_font).pack(pady=(10, 0))
    password_entry = tk.Entry(win, show="*")
    password_entry.pack()

    tk.Label(win, text="Retype Password", font=label_font).pack(pady=(10, 0))
    repassword_entry = tk.Entry(win, show="*")
    repassword_entry.pack()

    tk.Button(win, text="Sign Up", command=submit, width=20).pack(pady=20)
    tk.Button(win, text="Back", command=lambda: [win.destroy(), navigate.to_welcome()]).pack()

    win.mainloop()
