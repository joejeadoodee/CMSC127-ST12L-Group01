import tkinter as tk
from src import organization, navigate
from src.utils import center_window


def home():
    def handle_manage_members():
        root.destroy()
        navigate.to_manage_members()

    def handle_manage_fees():
        root.destroy()
        navigate.to_manage_fees()

    def handle_view_reports():
        root.destroy()
        navigate.to_view_reports()

    def handle_logout():
        root.destroy()
        navigate.to_welcome()

    root = tk.Tk()
    root.title("Organization Home")
    root.geometry("400x400")
    center_window(root, 400, 400)

    welcome_label = tk.Label(root, text=f"WELCOME, {organization.name}", font=("Arial", 14))
    welcome_label.pack(pady=10)

    btn_members = tk.Button(root, text="Manage Members", width=25, command=handle_manage_members)
    btn_members.pack(pady=5)

    btn_fees = tk.Button(root, text="Manage Fees", width=25, command=handle_manage_fees)
    btn_fees.pack(pady=5)

    btn_reports = tk.Button(root, text="View Reports", width=25, command=handle_view_reports)
    btn_reports.pack(pady=5)

    btn_logout = tk.Button(root, text="Logout", width=25, command=handle_logout)
    btn_logout.pack(pady=10)

    root.mainloop()


def manage_members():
    def go_back():
        root.destroy()
        navigate.to_home('organization')

    root = tk.Tk()
    root.title("Manage Members")
    root.geometry("400x400")
    center_window(root, 400, 400)


    tk.Label(root, text="👥 MANAGE MEMBERS", font=("Arial", 14)).pack(pady=10)

    options = [
        "Add Member",
        "Update Member",
        "Delete Member",
        "Search Members",
        "Update Member Role/Status",
    ]

    for option in options:
        tk.Button(root, text=option, width=30).pack(pady=3)

    tk.Button(root, text="Back", width=25, command=go_back).pack(pady=10)

    root.mainloop()


def manage_fees():
    def go_back():
        root.destroy()
        navigate.to_home('organization')

    root = tk.Tk()
    root.title("Manage Fees")
    root.geometry("400x400")
    center_window(root, 400, 400)


    tk.Label(root, text="💰 MANAGE FEES", font=("Arial", 14)).pack(pady=10)

    options = [
        "Add Membership Fee",
        "Update Membership Fee",
        "Delete Membership Fee",
        "View Fee Records",
        "Generate Financial Report"
    ]

    for option in options:
        tk.Button(root, text=option, width=30).pack(pady=3)

    tk.Button(root, text="Back", width=25, command=go_back).pack(pady=10)

    root.mainloop()


def view_reports():
    def go_back():
        root.destroy()
        navigate.to_home('organization')

    root = tk.Tk()
    root.title("View Reports")
    root.geometry("400x500")
    center_window(root, 400, 400)


    tk.Label(root, text="📊 VIEW REPORTS", font=("Arial", 14)).pack(pady=10)

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

    for option in options:
        tk.Button(root, text=option, width=35).pack(pady=3)

    tk.Button(root, text="Back", width=25, command=go_back).pack(pady=10)

    root.mainloop()
