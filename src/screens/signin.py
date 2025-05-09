from src.decorators import screen
   
@screen
def sign_in_admin():
    print("SIGNING IN AS ADMIN...")
    username = input("Enter username: ")
    password = input("Enter password: ")

    # ADD VALIDATION AND UPDATE DATABASE
    print("SIGNED IN!")
    print("-" * 10)
    print("REDIRECTING TO HOME SCREEN...")

@screen
def sign_in_organization():
    print("SIGNING IN AS ORGANIZATION...")
    username = input("Enter username: ")
    password = input("Enter password: ")

    # ADD VALIDATION AND UPDATE DATABASE
    print("SIGNED IN!")
    print("-" * 10)
    print("REDIRECTING TO HOME SCREEN...")

@screen
def sign_in_member():
    print("SIGNING IN AS MEMBER...")
    username = input("Enter username: ")
    password = input("Enter password: ")

    # ADD VALIDATION AND UPDATE DATABASE
    print("SIGNED IN!")
    print("-" * 10)
    print("REDIRECTING TO HOME SCREEN...")
