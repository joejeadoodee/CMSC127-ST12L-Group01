import tkinter as tk
from tkinter import messagebox
from tkinter import font

from src.decorators import screen
import src.mariadb_connector as db
from src import navigate, member, organization
from src.utils import center_window


@screen
def sign_in_organization():
    win = tk.Tk()
    win.title("Organization Login")
    win.geometry("400x400")
    center_window(win, 400, 400)

    heading_font = font.Font(family='Georgia', size=16, weight='bold')
    label_font = font.Font(family='Arial', size=12)

    tk.Label(win, text="Login as Organization", font=heading_font, fg="dark green").pack(pady=15)

    frame = tk.Frame(win)
    frame.pack(pady=10)

    tk.Label(frame, text="Name:", font=label_font).grid(row=0, column=0, sticky='e', pady=5)
    name_entry = tk.Entry(frame, width=25)
    name_entry.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Password:", font=label_font).grid(row=1, column=0, sticky='e', pady=5)
    password_entry = tk.Entry(frame, width=25, show='*')
    password_entry.grid(row=1, column=1, pady=5)

    def submit():
        name = name_entry.get()
        password = password_entry.get()
        db.cursor.execute(f"SELECT * FROM ORGANIZATION WHERE name='{name}' AND password='{password}'")
        row = db.cursor.fetchone()

        if row is None:
            messagebox.showerror("Login Failed", "Invalid credentials.")
        else:
            organization.organization_id = row[0]
            organization.name = row[1]
            organization.number_of_members = row[3]
            win.destroy()
            navigate.to_home('organization')

    tk.Button(win, text="Login", command=submit, font=label_font).pack(pady=10)
    tk.Button(win, text="Back", command=lambda: (win.destroy(), navigate.to_welcome()), font=label_font).pack()

    win.mainloop()

@screen
def sign_in_member():
    win = tk.Tk()
    win.title("Member Login")
    win.geometry("400x400")
    center_window(win, 400, 400)

    heading_font = font.Font(family='Georgia', size=16, weight='bold')
    label_font = font.Font(family='Arial', size=12)

    tk.Label(win, text="Login as Member", font=heading_font, fg="dark green").pack(pady=15)

    frame = tk.Frame(win)
    frame.pack(pady=10)

    tk.Label(frame, text="Username:", font=label_font).grid(row=0, column=0, sticky='e', pady=5)
    username_entry = tk.Entry(frame, width=25)
    username_entry.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Password:", font=label_font).grid(row=1, column=0, sticky='e', pady=5)
    password_entry = tk.Entry(frame, width=25, show='*')
    password_entry.grid(row=1, column=1, pady=5)

    def submit():
        username = username_entry.get()
        password = password_entry.get()
        db.cursor.execute(f"SELECT * FROM MEMBER WHERE username='{username}' AND password='{password}'")
        row = db.cursor.fetchone()

        if row is None:
            messagebox.showerror("Login Failed", "Invalid credentials.")
        else:
            member.member_id = row[0]
            member.username = row[1]
            member.name = row[2]
            member.batch = row[4]
            member.status = row[5]
            member.gender = row[6]
            member.is_admin = row[7]
            win.destroy()
            navigate.to_home('member')

    tk.Button(win, text="Login", command=submit, font=label_font).pack(pady=10)
    tk.Button(win, text="Back", command=lambda: (win.destroy(), navigate.to_welcome()), font=label_font).pack()

    win.mainloop()
