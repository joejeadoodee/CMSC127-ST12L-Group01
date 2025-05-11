from src.screens import welcome
from src.screens.member import member_home
from src.screens.member.member_profile import view_profile
from src.screens.member.member_dues import view_dues
from src.screens.member.member_organizations import view_organizations

from src.screens.organization import organization_home
from src.screens.organization.org_members import manage_members
from src.screens.organization.org_fees import manage_fees
from src.screens.organization.org_reports import view_reports

def to_home(user_type):
    if user_type == 'member':
        member_home.home()
    if user_type == 'organization':
        organization_home.home()

def to_welcome():
    welcome.welcome()


def to_view_profile():
    view_profile()

def to_view_dues():
    view_dues()

def to_view_organizations():
    view_organizations()

def to_manage_fees():
    manage_fees()

def to_manage_members():
    manage_members()

def to_view_reports():
    view_reports()
