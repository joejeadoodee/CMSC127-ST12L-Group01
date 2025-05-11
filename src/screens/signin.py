from src.decorators import screen
from src import navigate
import src.mariadb_connector as db
from src import member, organization
   
@screen
def sign_in_admin():
    print("SIGNING IN AS ADMIN...")
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")

        db.cursor.execute("SELECT * FROM MEMBER WHERE username='{x}' AND password='{y}' AND is_admin".format(x=username, y=password))
        row = db.cursor.fetchone()
        if row == None:
            print("-" * 10)
            print("Invalid credentials")
            retry = input("Retry (Y/n): ")
            if retry in "Nn":
                return navigate.to_welcome()
            else:
                continue

        member.member_id = row[0]
        member.username = row[1]
        member.name = row[2]
        member.batch = row[4]
        member.status = row[5]
        member.gender = row[6]
        member.is_admin = row[7]
        break

    print("-" * 10)
    print("SIGNED IN!")
    print("REDIRECTING TO HOME SCREEN...")
    navigate.to_home('member')

@screen
def sign_in_organization():
    print("SIGNING IN AS ORGANIZATION...")
    while True:
        name = input("Enter name: ")
        password = input("Enter password: ")

        db.cursor.execute("SELECT * FROM ORGANIZATION WHERE name='{x}' AND password='{y}'".format(x=name, y=password))
        row = db.cursor.fetchone()
        if row == None:
            print("-" * 10)
            print("Invalid credentials")
            retry = input("Retry (Y/n): ")
            if retry in "Nn":
                return navigate.to_welcome()
            else:
                continue

        organization.member_id = row[0]
        organization.name = row[1]
        organization.number_of_members = row[3]
        break

    print("-" * 10)
    print("SIGNED IN!")
    print("REDIRECTING TO HOME SCREEN...")
    navigate.to_home('organization')

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

        member.member_id = row[0]
        member.username = row[1]
        member.name = row[2]
        member.batch = row[4]
        member.status = row[5]
        member.gender = row[6]
        member.is_admin = row[7]
        break

    print("-" * 10)
    print("SIGNED IN!")
    print("REDIRECTING TO HOME SCREEN...")
    navigate.to_home('member')
