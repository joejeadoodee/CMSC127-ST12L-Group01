import tkinter as tk
from src.decorators import screen
import src.mariadb_connector as db
from src import member, navigate
from src.utils import center_window

@screen
def view_organizations():
    window = tk.Tk()  # Root window
    window.title("My Organizations")
    window.geometry("500x400")
    center_window(window, 500, 400)

    tk.Label(window, text="=== MY ORGANIZATIONS ===", font=("Arial", 16, "bold")).pack(pady=10)

    try:
        if db.conn is None or db.cursor is None:
            db.connect()

        member_id = member.member_id
        username = member.username

        if not member_id or not username:
            tk.Label(window, text="Error: No member is currently logged in.").pack()
            return

        query = """
        SELECT O.name, S.role, S.semester, S.school_year
        FROM SERVES S
        JOIN ORGANIZATION O ON S.organization_id = O.organization_id
        WHERE S.member_id = ? AND S.username = ?
        ORDER BY S.school_year DESC, S.semester DESC;
        """
        db.cursor.execute(query, (member_id, username))
        results = db.cursor.fetchall()

        if not results:
            tk.Label(window, text="You are not currently part of any organizations.").pack(pady=10)
        else:
            for i, (org_name, role, semester, year) in enumerate(results, 1):
                org_info = (
                    f"{i}. Organization: {org_name}\n"
                    f"   Role: {role}\n"
                    f"   Joined: {semester} {year}\n"
                )
                tk.Label(window, text=org_info, justify="left", anchor="w").pack(anchor="w", padx=20, pady=5)

    except Exception as e:
        tk.Label(window, text=f"An error occurred: {e}", fg="red").pack()

    tk.Button(window, text="Return", command=lambda: (window.destroy(), navigate.to_home('member'))).pack(pady=20)

    window.mainloop()
