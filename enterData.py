import psycopg2
from datetime import datetime, timedelta
import random

# Postgres database connection details
dbname = 'healthtracker'
user = 'postgres'
password = 'mypassword'
host = 'db'
port = '5000'

# Connect to Postgres database
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)


# Define a function to generate a random value within a range
def generate_random_value(start, end):
    return round(random.uniform(start, end), 1)


# Get the current date and time
now = datetime.now()

# Generate 10 rows of dummy data
for i in range(1, 11):
    # Increment the date by one day for each row
    date = (now + timedelta(days=i)).strftime('%Y-%m-%d')

    # Generate random values for each column
    sleep = random.randint(1, 13)
    calories = random.randint(1800, 3000)
    step_count = random.randint(3000, 10000)
    weight = random.randint(60, 70)
    bodyfat = random.randint(8, 13)
    mood = random.randint(1, 10)
    protein = generate_random_value(150, 300)
    carbs = generate_random_value(150, 300)
    fats = generate_random_value(60, 120)

    # Insert the row into the "health_metric" table
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO health_metric (user_id, date, sleep, calories, step_count, weight, bodyfat, mood, protein, carbs, fats) VALUES (1, '{date}', {sleep}, {calories}, {step_count}, {weight}, {bodyfat}, {mood}, {protein}, {carbs}, {fats})")
    conn.commit()
    cur.close()

# Close the database connection
conn.close()
