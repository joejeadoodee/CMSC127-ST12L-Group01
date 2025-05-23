from src.decorators import screen
from src import navigate
import src.mariadb_connector as db

# Sign up as a Member

@screen
def sign_up_member():
    print("SIGNING UP AS MEMBER...")
    name = input("Enter your full name: ")
    username = input("Enter username: ")
    batch = input("Enter batch year: ")
    gender = input("Enter gender: ")
    password = input("Enter password: ")
    repassword = input("Retype password: ")

    if password != repassword:
        print("Passwords do not match! Please try again.")
        return sign_up_member()

    try:
        insert_query = """
            INSERT INTO MEMBER (username, name, password, batch, status, gender, is_admin)
            VALUES ('{0}', '{1}', '{2}', {3}, '{4}', '{5}', {6})
        """.format(username, name, password, int(batch), 'Active', gender, 'FALSE')
        
        db.cursor.execute(insert_query)
    except Exception as e:
        print("An error occurred while signing up:", e)
        return

    print("SIGNED UP AS MEMBER!")
    print("-" * 10)
    print("REDIRECTING TO HOME SCREEN...")
    return navigate.to_welcome()


# Sign up as an Organization
@screen
def sign_up_org():
    print("SIGNING UP AS ORGANIZATION...")
    org_name = input("Enter organization name: ")
    password = input("Enter password: ")
    repassword = input("Retype password: ")

    if password != repassword:
        print("Passwords do not match! Please try again.")
        return sign_up_org()

    try:
        insert_query = """
            INSERT INTO ORGANIZATION (name, password, number_of_members)
            VALUES ('{0}', '{1}', {2})
        """.format(org_name, password, 0)

        db.cursor.execute(insert_query)
    except Exception as e:
        print("An error occurred while signing up:", e)
        return

    print("SIGNED UP AS ORGANIZATION!")
    print("-" * 10)
    print("REDIRECTING TO HOME SCREEN...")
    return navigate.to_welcome()

