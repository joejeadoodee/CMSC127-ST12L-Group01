from src.decorators import screen
from src import member, navigate

@screen
def view_profile():
    print("MY PROFILE")
    # insert code here
    input("Press Enter to return...")
    navigate.to_home('member')

