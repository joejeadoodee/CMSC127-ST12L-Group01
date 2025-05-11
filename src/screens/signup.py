from src.decorators import screen
from src import navigate

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

    # ADD VALIDATION AND UPDATE DATABASE

    if password != repassword:
        print("Passwords do not match! Please try again.")
        return sign_up_member()

    # Assuming there's a function for inserting data into a database
    # db.insert_member(name, username, batch, gender, password)

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

    # ADD VALIDATION AND UPDATE DATABASE

    if password != repassword:
        print("Passwords do not match! Please try again.")
        return sign_up_org()

    # Assuming there's a function for inserting data into a database
    # db.insert_organization(org_name, password)

    print("SIGNED UP AS ORGANIZATION!")
    print("-" * 10)
    print("REDIRECTING TO HOME SCREEN...")
    return navigate.to_welcome()
