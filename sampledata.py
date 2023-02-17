import psycopg2

data = [
    {
        "date": "2023-02-16",
        "calories": 2000,
        "protein": 150,
        "carbs": 250,
        "fats": 110,
        "sleep": 8,
        "mood": 7,
    },
    {
        "date": "2023-02-15",
        "calories": 2100,
        "protein": 150,
        "carbs": 250,
        "fats": 80,
        "sleep": 7,
        "mood": 6,
    },
    {
        "date": "2023-02-14",
        "calories": 2300,
        "protein": 150,
        "carbs": 250,
        "fats": 90,
        "sleep": 8,
        "mood": 5,
    },
    {
        "date": "2023-02-13",
        "calories": 1800,
        "protein": 120,
        "carbs": 220,
        "fats": 100,
        "sleep": 10,
        "mood": 9,
    },
    {
        "date": "2023-02-12",
        "calories": 2100,
        "protein": 140,
        "carbs": 230,
        "fats": 120,
        "sleep": 6,
        "mood": 6,
    },
    {
        "date": "2023-02-11",
        "calories": 2000,
        "protein": 120,
        "carbs": 280,
        "fats": 70,
        "sleep": 5,
        "mood": 8,
    },
    {
        "date": "2023-02-10",
        "calories": 2200,
        "protein": 180,
        "carbs": 240,
        "fats": 150,
        "sleep": 8,
        "mood": 7,
    }
]

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
    CREATE TABLE IF NOT EXISTS health (
        id serial PRIMARY KEY,
        date DATE,
        calories INTEGER,
        protein INTEGER,
        carbs INTEGER,
        fats INTEGER,
        sleep INTEGER,
        mood INTEGER
    );
""")

# Iterate over the data and insert into the table
for row in data:
    query = "INSERT INTO health (date, calories, protein, carbs, fats, sleep, mood) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (
        row["date"],
        row["calories"],
        row["protein"],
        row["carbs"],
        row["fats"],
        row["sleep"],
        row["mood"]
    )
    cur.execute(query, values)

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
