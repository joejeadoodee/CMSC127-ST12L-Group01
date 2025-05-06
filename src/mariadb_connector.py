import mariadb 

def connect():
    print("Connecting to mariadb -------")
    conn = mariadb.connect( 
        user="jojolanot", 
        password="jojolanot", 
        host="localhost", 
        database="org"
    ) 

    cur = conn.cursor() 
    print("CONNECTED ------ \n\n")
