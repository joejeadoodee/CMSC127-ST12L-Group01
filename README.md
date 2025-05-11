# STUDENT ORGANIZATION MANAGEMENT SYSTEM

## Introduction
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.


## Project Description
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Technology Stack
- **Programming Language**:
- **Database**:

## Core Features
### 1. Membership Management
- Add, update, delete, and search for members.
- Assign roles (President, Treasurer, Member, etc.).
- Track membership status: `Active`, `Inactive`, `Suspended`, `Expelled`, `Alumni`.
- A student can be part of multiple organizations.

### 2. Fees Management
- Manage membership fees and dues per member and organization.
- Generate financial reports.

## Reports to be Generated

1. View all members of the organization by role, status, gender, degree program, batch (year of membership), and committee. 
2. View members for a given organization with unpaid membership fees or dues for a given semester and academic year.
3. View a member’s unpaid membership fees or dues for all their organizations.
4. View all executive committee members of a given organization for a given academic year.
5. View all Presidents (or any other role) of a given organization for every academic year in reverse chronological order (current to past).
6. View all late payments made by all members of a given organization for a given semester and academic year.
7. View the percentage of active vs inactive members of a given organization for the last n semesters. 
8. View all alumni members of a given organization as of a given date.
9. View the total amount of unpaid and paid fees or dues of a given organization as of a given date.
10. View the member/s with the highest debt of a given organization for a given semester.

## Project Progress

- **Milestone 1**: Entity-Relationship Diagram 
- **Milestone 2**: Revised Entity-Relationship Diagram to relational table 
- **Milestone 3**: Create tables, core functionalities implementation (`add`, `update`, etc.) in progress

## How to setup
1. Clone the repository:
```bash
git clone https://github.com/joejeadoodee/CMSC127-ST12L-Group01.git
```

2. Run the ff commands:
```bash
curl -LsSO https://r.mariadb.com/downloads/mariadb_repo_setup

echo "c4a0f3dade02c51a6a28ca3609a13d7a0f8910cccbb90935a2f218454d3a914a  mariadb_repo_setup" \
    | sha256sum -c -

chmod +x mariadb_repo_setup
sudo ./mariadb_repo_setup
sudo apt install libmariadb3 libmariadb-dev

sudo apt install python3.12-venv
python3 -m venv myenv
``` 

3. Grant permission on "org" database to user "jojolanot". Make sure "org" exists.
```bash
sudo mariadb

USE org
# Paste milestone3.sql in the command line to populate database
GRANT ALL PRIVILEGES ON org.* TO 'jojolanot'@'%';
```


## How to Run
1. Run virtual environment
```bash
source myenv/bin/activate
pip install -r requirements.txt
```
2. Run main.py
```bash
python3 main.py
```