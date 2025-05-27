import tkinter as tk
from tkinter import messagebox
from src import member, navigate
import src.mariadb_connector as db
from src.utils import center_window

def view_profile():
    window = tk.Tk()
    window.title("My Profile")
    window.geometry("400x350")
    center_window(window, 400, 400)


    tk.Label(window, text="=== MY PROFILE ===", font=("Arial", 16, "bold")).pack(pady=10)

    # Fetch degree program
    degree_program = "Not available"
    try:
        db.cursor.execute("""
            SELECT degree_program
            FROM MEMBER_DEGREE_PROGRAM
            WHERE member_id = %s
        """, (member.member_id,))
        result = db.cursor.fetchone()
        if result:
            degree_program = result[0]
    except Exception as e:
        degree_program = f"Error: {e}"

    # Profile info dictionary
    profile_fields = {
        "Name": member.name or "Not provided",
        "Username": member.username or "Not provided",
        "Batch": member.batch or "Not provided",
        "Status": member.status or "Not provided",
        "Gender": member.gender or "Not provided",
        "Degree Program": degree_program
    }

    # Display profile fields
    for label, value in profile_fields.items():
        tk.Label(window, text=f"{label:<15}: {value}", anchor='w', justify='left').pack(anchor='w', padx=20, pady=2)

    # Return button
    tk.Button(window, text="Return", command=lambda: (window.destroy(), navigate.to_home('member'))).pack(pady=20)
