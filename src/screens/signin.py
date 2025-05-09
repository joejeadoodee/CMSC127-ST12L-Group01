from src.decorators import screen
from src import navigate
import src.mariadb_connector as db
from src import provider
   
@screen
def sign_in_admin():
    print("SIGNING IN AS ADMIN...")
    username = input("Enter username: ")
    password = input("Enter password: ")

    # ADD VALIDATION AND UPDATE DATABASE
    print("SIGNED IN!")
    print("-" * 10)
    print("REDIRECTING TO HOME SCREEN...")
    navigate.to_home()

@screen
def sign_in_organization():
    print("SIGNING IN AS ORGANIZATION...")
    username = input("Enter username: ")
    password = input("Enter password: ")

    # ADD VALIDATION AND UPDATE DATABASE
    print("SIGNED IN!")
    print("-" * 10)
    print("REDIRECTING TO HOME SCREEN...")
    navigate.to_home()

@screen
def sign_in_member():
    print("SIGNING IN AS MEMBER...")
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")

        db.cursor.execute("SELECT * FROM MEMBER WHERE username='{x}' AND password='{y}'".format(x=username, y=password))
        row = db.cursor.fetchone()
        if row == None:
            print("-" * 10)
            print("Invalid credentials")
            retry = input("Retry (Y/n): ")
            if retry in "Nn":
                return navigate.to_welcome()
            else:
                continue

        provider.member_id = row[0]
        provider.username = row[1]
        provider.name = row[2]
        provider.batch = row[4]
        provider.status = row[5]
        provider.gender = row[6]
        provider.is_admin = row[7]
        break

    print("-" * 10)
    print("SIGNED IN!")
    print("REDIRECTING TO HOME SCREEN...")
    navigate.to_home()
