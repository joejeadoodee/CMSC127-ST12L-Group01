import mariadb 

cursor = None
conn = None 

def connect():
    global cursor, conn 
    print("Connecting to mariadb -------")
    conn = mariadb.connect( 
        user="jojolanot", 
        password="jojolanot", 
        host="localhost", 
        database="org"
    ) 

    cursor = conn.cursor() 
    print("CONNECTED ------")
