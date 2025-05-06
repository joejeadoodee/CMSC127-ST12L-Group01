from src import screens, mariadb_connector

if __name__ == "__main__":
    mariadb_connector.connect()

    while True:
        screens.home()
        user_input = input("Enter option: ")
        
        if user_input == "3":
            break
        
        print("\n")


