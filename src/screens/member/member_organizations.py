from src.decorators import screen
import src.mariadb_connector as db
from src import member, navigate

@screen
def view_organizations():
    print("MY ORGANIZATIONS\n")
    
    try:
        if db.conn is None or db.cursor is None:
            db.connect()

        member_id = member.member_id
        username = member.username

        if not member_id or not username:
            print("Error: No member is currently logged in.")
            input("\nPress Enter to go back...")
            return navigate.to_home('member')
        
        query = """
        SELECT O.name, S.role, S.semester, S.school_year
        FROM SERVES S
        JOIN ORGANIZATION O ON S.organization_id = O.organization_id
        WHERE S.member_id = ? AND S.username = ?
        ORDER BY S.school_year DESC, S.semester DESC;
        """
        db.cursor.execute(query, (member_id, username))
        results = db.fetchall()

        if not results:
            print("You are not currently part of any organizations.")
        else:
            for i, (org_name, role, semester, year) in enumerate(results, 1):
                print(f"{i}. Organization: {org_name}")
                print(f"   Role: {role}")
                print(f"   Joined: {semester} {year}\n")

    except Exception as e:
        print(f"An error occurred: {e}")

    input("Press Enter to go back...") 
    navigate.to_home('member')

