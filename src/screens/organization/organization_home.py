import tkinter as tk
from tkinter import messagebox
from src.decorators import screen
from src import organization, navigate

@screen
def home():
    root = tk.Tk()
    root.title(f"Welcome, {organization.name}")
    root.geometry("300x250")

    def on_manage_members():
        root.destroy()
        navigate.to_manage_members()

    def on_manage_fees():
        root.destroy()
        navigate.to_manage_fees()

    def on_view_reports():
        root.destroy()
        navigate.to_view_reports()

    def on_logout():
        root.destroy()
        navigate.to_welcome()

    label = tk.Label(root, text=f"WELCOME, {organization.name}", font=("Arial", 14))
    label.pack(pady=20)

    btn_members = tk.Button(root, text="Manage Members", width=25, command=on_manage_members)
    btn_members.pack(pady=5)

    btn_fees = tk.Button(root, text="Manage Fees", width=25, command=on_manage_fees)
    btn_fees.pack(pady=5)

    btn_reports = tk.Button(root, text="View Reports", width=25, command=on_view_reports)
    btn_reports.pack(pady=5)

    btn_logout = tk.Button(root, text="Logout", width=25, command=on_logout)
    btn_logout.pack(pady=20)

    root.mainloop()


@screen
def manage_members():
    window = tk.Tk()
    window.title("👥 Manage Members")
    window.geometry("300x300")

    def on_add_member():
        window.destroy()
        navigate.to_add_member()

    def on_update_member():
        window.destroy()
        navigate.to_update_member()

    def on_delete_member():
        window.destroy()
        navigate.to_delete_member()

    def on_search_members():
        window.destroy()
        navigate.to_search_members()

    def on_update_role_status():
        window.destroy()
        navigate.to_update_role_status()

    def on_back():
        window.destroy()
        navigate.to_home('organization')

    tk.Label(window, text="👥 MANAGE MEMBERS", font=("Arial", 14)).pack(pady=15)

    tk.Button(window, text="Add Member", width=25, command=on_add_member).pack(pady=5)
    tk.Button(window, text="Update Member", width=25, command=on_update_member).pack(pady=5)
    tk.Button(window, text="Delete Member", width=25, command=on_delete_member).pack(pady=5)
    tk.Button(window, text="Search Members", width=25, command=on_search_members).pack(pady=5)
    tk.Button(window, text="Update Member Role/Status", width=25, command=on_update_role_status).pack(pady=5)
    tk.Button(window, text="Back", width=25, command=on_back).pack(pady=10)

    window.mainloop()


@screen
def manage_fees():
    window = tk.Tk()
    window.title("💰 Manage Fees")
    window.geometry("300x250")

    def on_add_fee():
        window.destroy()
        navigate.to_add_fee()

    def on_update_fee():
        window.destroy()
        navigate.to_update_fee()

    def on_delete_fee():
        window.destroy()
        navigate.to_delete_fee()

    def on_view_fees():
        window.destroy()
        navigate.to_view_fees()

    def on_back():
        window.destroy()
        navigate.to_home('organization')

    tk.Label(window, text="💰 MANAGE FEES", font=("Arial", 14)).pack(pady=15)

    tk.Button(window, text="Add Membership Fee", width=25, command=on_add_fee).pack(pady=5)
    tk.Button(window, text="Update Membership Fee", width=25, command=on_update_fee).pack(pady=5)
    tk.Button(window, text="Delete Membership Fee", width=25, command=on_delete_fee).pack(pady=5)
    tk.Button(window, text="View Fee Records", width=25, command=on_view_fees).pack(pady=5)
    tk.Button(window, text="Back", width=25, command=on_back).pack(pady=10)

    window.mainloop()


@screen
def view_reports():
    window = tk.Tk()
    window.title("📊 View Reports")
    window.geometry("350x450")

    def nav_to_report(option):
        window.destroy()
        report_routes = {
            '1': navigate.to_member_overview,
            '2': navigate.to_unpaid_members,
            '3': navigate.to_executive_committee,
            '4': navigate.to_historical_roles,
            '5': navigate.to_late_payments,
            '6': navigate.to_member_status_analytics,
            '7': navigate.to_alumni_report,
            '8': navigate.to_financial_summary,
            '9': navigate.to_member_highest_debt,
        }
        if option in report_routes:
            report_routes[option]()
        else:
            messagebox.showerror("Invalid Option", "Invalid report selection.")

    tk.Label(window, text="📊 VIEW REPORTS", font=("Arial", 14)).pack(pady=15)

    tk.Button(window, text="1. Member Overview", width=30, command=lambda: nav_to_report('1')).pack(pady=3)
    tk.Button(window, text="2. Unpaid Members", width=30, command=lambda: nav_to_report('2')).pack(pady=3)
    tk.Button(window, text="3. Executive Committee", width=30, command=lambda: nav_to_report('3')).pack(pady=3)
    tk.Button(window, text="4. Historical Roles", width=30, command=lambda: nav_to_report('4')).pack(pady=3)
    tk.Button(window, text="5. Late Payments", width=30, command=lambda: nav_to_report('5')).pack(pady=3)
    tk.Button(window, text="6. Member Status Analytics", width=30, command=lambda: nav_to_report('6')).pack(pady=3)
    tk.Button(window, text="7. Alumni Report", width=30, command=lambda: nav_to_report('7')).pack(pady=3)
    tk.Button(window, text="8. Financial Summary", width=30, command=lambda: nav_to_report('8')).pack(pady=3)
    tk.Button(window, text="9. Member with Highest Debt", width=30, command=lambda: nav_to_report('9')).pack(pady=3)

    tk.Button(window, text="Back", width=30, command=lambda: [window.destroy(), navigate.to_home('organization')]).pack(pady=15)

    window.mainloop()
