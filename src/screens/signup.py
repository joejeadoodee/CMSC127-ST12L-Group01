from src.decorators import screen
from src import navigate
   
@screen
def sign_up():
    print("SIGNING UP...")
    name = input("Enter your full name: ")
    username = input("Enter username: ")
    batch = input("Enter batch year: ")
    gender = input("Enter gender: ")
    password = input("Enter password: ")
    repassword = input("Retype password: ")

    # ADD VALIDATION AND UPDATE DATABASE
    print("SIGNED UP!")
    print("-" * 10)
    print("REDIRECTING TO HOME SCREEN...")
    return navigate.to_welcome()