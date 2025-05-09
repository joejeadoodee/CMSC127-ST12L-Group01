from src.screens.welcome import welcome
from src.mariadb_connector import connect

if __name__ == "__main__":
    connect()
    welcome()
    print("-" * 10)
