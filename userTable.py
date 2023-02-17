import psycopg2

# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    database="healthtracker",
    user="postgres",
    password="mysecretpassword"
)

# Open a cursor to perform database operations
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id serial PRIMARY KEY,
        first_name VARCHAR(40) NOT NULL,
        last_name VARCHAR(40) NOT NULL,
        email VARCHAR(254) NOT NULL,
        password VARCHAR NOT NULL
    );
""")


conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

print("Success")
