import tkinter as tk
from tkinter import messagebox
from src import member, navigate
from src.utils import center_window


def home():
    def handle_view_profile():
        root.destroy()
        navigate.to_view_profile()

    def handle_view_dues():
        root.destroy()
        navigate.to_view_dues()

    def handle_view_organizations():
        root.destroy()
        navigate.to_view_organizations()

    def handle_logout():
        root.destroy()
        navigate.to_welcome()

    root = tk.Tk()
    root.title("Home")
    root.geometry("400x400")
    center_window(root, 400, 400)


    welcome_label = tk.Label(root, text=f"WELCOME, {member.name}", font=("Arial", 14))
    welcome_label.pack(pady=10)

    btn_profile = tk.Button(root, text="View My Profile", width=25, command=handle_view_profile)
    btn_profile.pack(pady=5)

    btn_dues = tk.Button(root, text="View My Financial Obligations", width=25, command=handle_view_dues)
    btn_dues.pack(pady=5)

    btn_orgs = tk.Button(root, text="View My Organizations", width=25, command=handle_view_organizations)
    btn_orgs.pack(pady=5)

    btn_logout = tk.Button(root, text="Logout", width=25, command=handle_logout)
    btn_logout.pack(pady=10)

    root.mainloop()
