from src.decorators import screen
import src.mariadb_connector as db
from src import member, navigate

@screen
def view_organizations():
    print("MY ORGANIZATIONS")
    # insert code here
    navigate.to_home('member')

