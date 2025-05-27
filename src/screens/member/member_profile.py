from src.decorators import screen
from src import member, navigate
import src.mariadb_connector as db

@screen
def view_profile():
    print("=== MY PROFILE ===\n")

    # Default if no degree program is found
    degree_program = "Not available"

    try:
        # Secure query using parameterized SQL
        db.cursor.execute("""
            SELECT degree_program
            FROM MEMBER_DEGREE_PROGRAM
            WHERE member_id = %s
        """, (member.member_id,))
        result = db.cursor.fetchone()

        if result:
            degree_program = result[0]

    except Exception as e:
        degree_program = f"Error retrieving program: {e}"

    # Print profile details
    profile_fields = {
        "Name": member.name or "Not provided",
        "Username": member.username or "Not provided",
        "Batch": member.batch or "Not provided",
        "Status": member.status or "Not provided",
        "Gender": member.gender or "Not provided",
        "Degree Program": degree_program
    }

    for label, value in profile_fields.items():
        print(f"{label:<15}: {value}")

    input("\nPress Enter to return...")
    navigate.to_home('member')
