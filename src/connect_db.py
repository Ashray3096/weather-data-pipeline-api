import psycopg2
from psycopg2 import sql

def connect_to_postgres(dbname, user, password, host='localhost', port=5432):
    try:
        # Create a connection to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        
        # Create a cursor object
        cursor = conn.cursor()
        
        print("Connected to the PostgreSQL database.")
        
        return conn, cursor
    except Exception as error:
        print(f"Error connecting to PostgreSQL database: {error}")

# Usage
dbname = 'cropyielddb'
user = 'postgres'
password = 'root'
host = 'localhost'
port = '5432'

conn, cursor = connect_to_postgres(dbname, user, password, host, port)

# Remember to close the connection and cursor when done
cursor.close()
conn.close()
