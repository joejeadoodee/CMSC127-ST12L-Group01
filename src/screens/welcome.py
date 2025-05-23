import tkinter as tk
from tkinter import font

from src.decorators import screen
import src.mariadb_connector as db
from src.screens.signup import sign_up_member, sign_up_org
from src.screens.signin import sign_in_member, sign_in_organization
import sys
from src.utils import center_window

@screen
def welcome():
    # Create main window
    win = tk.Tk()
    win.title("Student Organization Management System")
    win.geometry("400x400")
    center_window(win, 400, 400)

    # Define fonts
    heading_font = font.Font(family='Georgia', size=18, weight='bold')
    button_font = font.Font(family='Arial', size=12)

    # Create main frame
    main_frame = tk.Frame(win)
    main_frame.pack(fill='both', expand=True)

    # Heading label
    heading = tk.Label(main_frame, text="STUDENT ORGANIZATION\nMANAGEMENT SYSTEM", font=heading_font, fg="dark green")
    heading.pack(pady=30)

    # Button actions
    def login_organization():
        win.destroy()
        sign_in_organization()

    def login_member():
        win.destroy()
        sign_in_member()

    def signup_organization():
        win.destroy()
        sign_up_org()

    def signup_member():
        win.destroy()
        sign_up_member()

    def exit_app():
        win.destroy()
        sys.exit()

    # Buttons
    buttons = [
        ("Log in as Organization", login_organization),
        ("Log in as Member", login_member),
        ("Sign up as Organization", signup_organization),
        ("Sign up as Member", signup_member),
        ("Exit", exit_app),
    ]

    for text, command in buttons:
        btn = tk.Button(main_frame, text=text, font=button_font, command=command, width=30)
        btn.pack(pady=5)

    win.mainloop()
