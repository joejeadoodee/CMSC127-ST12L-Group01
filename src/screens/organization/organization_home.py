import tkinter as tk
from src import organization, navigate
from src.utils import center_window

def home():
    window = tk.Tk()
    window.title("Home - Organization")
    window.geometry("400x400")
    center_window(window, 400, 400)

    tk.Label(window, text=f"WELCOME, {organization.name}", font=("Helvetica", 16)).pack(pady=10)

    buttons = [
        ("Manage Members", lambda: switch_screen(window, manage_members)),
        ("Manage Fees", lambda: switch_screen(window, manage_fees)),
        ("View Reports", lambda: switch_screen(window, view_reports)),
        ("Logout", lambda: logout(window))
    ]

    for text, cmd in buttons:
        tk.Button(window, text=text, width=30, command=cmd).pack(pady=5)

    window.mainloop()

def manage_members():
    window = tk.Tk()
    window.title("Manage Members")
    window.geometry("400x400")
    center_window(window, 400, 400)


    tk.Label(window, text="👥 MANAGE MEMBERS", font=("Helvetica", 16)).pack(pady=10)

    options = [
        "Add Member",
        "Update Member",
        "Delete Member",
        "Search Members",
        "Update Member Role/Status"
    ]

    for opt in options:
        tk.Button(window, text=opt, width=35).pack(pady=3)

    tk.Button(window, text="Back", width=25, command=lambda: switch_screen(window, home)).pack(pady=10)

    window.mainloop()

def manage_fees():
    window = tk.Tk()
    window.title("Manage Fees")
    window.geometry("400x400")
    center_window(window, 400, 400)

    tk.Label(window, text="💰 MANAGE FEES", font=("Helvetica", 16)).pack(pady=10)

    options = [
        "Add Membership Fee",
        "Update Membership Fee",
        "Delete Membership Fee",
        "View Fee Records",
        "Generate Financial Report"
    ]

    for opt in options:
        tk.Button(window, text=opt, width=35).pack(pady=3)

    tk.Button(window, text="Back", width=25, command=lambda: switch_screen(window, home)).pack(pady=10)

    window.mainloop()

def view_reports():
    window = tk.Tk()
    window.title("View Reports")
    window.geometry("400x500")
    center_window(window, 400, 500)

    tk.Label(window, text="📊 VIEW REPORTS", font=("Helvetica", 16)).pack(pady=10)

    options = [
        "Member Overview",
        "Unpaid Members",
        "Executive Committee",
        "Historical Roles",
        "Late Payments",
        "Member Status Analytics",
        "Alumni Report",
        "Financial Summary",
        "Member with Highest Debt"
    ]

    for opt in options:
        tk.Button(window, text=opt, width=35).pack(pady=3)

    tk.Button(window, text="Back", width=25, command=lambda: switch_screen(window, home)).pack(pady=10)

    window.mainloop()

def logout(window):
    window.destroy()
    # Optionally, call a welcome screen function here if you have one
    # For example: welcome()

def switch_screen(current_window, next_screen_func):
    current_window.destroy()
    next_screen_func()
