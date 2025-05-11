from src.screens import welcome
from src.screens.admin import admin_home
from src.screens.member import member_home
from src.screens.organization import organization_home

def to_home(user_type):
    if user_type == 'member':
        member_home.home()
    if user_type == 'admin':
        admin_home.home()
    if user_type == 'organzation':
        organization_home.home()

def to_welcome():
    welcome.welcome()