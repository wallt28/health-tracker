from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
import psycopg2
import plotly.graph_objs as go
import dotenv

from plotly.subplots import make_subplots

#? To do next: Create a log output that allows users to delete & update entries easily


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret" # Change this in production
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# PostgreSQL database connection
conn = psycopg2.connect(
    host="localhost",
    database="healthtracker",
    user="postgres",
    password="mysecretpassword"
)



# Define index route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get data from form
        date = request.form["date"]
        calories = request.form["calories"]
        protein = request.form["protein"]
        carbs = request.form["carbs"]
        fats = request.form["fats"]
        sleep = request.form["sleep"]
        mood = request.form["mood"]

        # Check if the date already exists in the data
        cur = conn.cursor()
        cur.execute("SELECT date FROM health WHERE date = %s", (date,))
        result = cur.fetchone()

        if result is not None:
            # Update existing entry
            cur.execute("UPDATE health SET calories = %s, protein = %s, carbs = %s, fats = %s, sleep = %s, mood = %s WHERE date = %s", (calories, protein, carbs, fats, sleep, mood, date))
        else:
            # Add new entry to database
            cur.execute("INSERT INTO health (date, calories, protein, carbs, fats, sleep, mood) VALUES (%s, %s, %s, %s, %s, %s, %s)", (date, calories, protein, carbs, fats, sleep, mood))

        conn.commit()
        cur.close()

    # Fetch data from database
    cur = conn.cursor()
    cur.execute("SELECT date, calories, protein, carbs, fats, sleep, mood FROM health ORDER BY date DESC")
    rows = cur.fetchall()
    cur.close()

    # Create list of dictionaries from fetched rows
    data = []
    for row in rows:
        data.append({
            "date": row[0],
            "calories": row[1],
            "protein": row[2],
            "carbs": row[3],
            "fats": row[4],
            "sleep": row[5],
            "mood": row[6]
        })

    # Create plotly figure
    fig = make_subplots(rows=2, cols=3, subplot_titles=("Calories", "Sleep", "Mood", "Fats", "Protein", "Carbs"))
    fig.add_trace(
        go.Scatter(
            x=[d["date"] for d in data],
            y=[d["calories"] for d in data],
            name="Calories",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=[d["date"] for d in data],
            y=[d["sleep"] for d in data],
            name="Sleep",
        ),
        row=1,
        col=2,
    )
    fig.add_trace(
        go.Scatter(
            x=[d["date"] for d in data],
            y=[d["mood"] for d in data],
            name="Mood",
        ),
        row=1,
        col=3,
    )
    fig.add_trace(
        go.Scatter(
            x=[d["date"] for d in data],
            y=[d["fats"] for d in data],
            name="Fats",
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=[d["date"] for d in data],
            y=[d["protein"] for d in data],
            name="Protein",
        ),
        row=2,
        col=2,
    )
    fig.add_trace(
        go.Scatter(
            x=[d["date"] for d in data],
            y=[d["carbs"] for d in data],
            name="Carbs",
        ),
        row=2,
        col=3,
    )
    fig.update_layout(height=600, title_text="Nutrional Data")


    # Convert plotly figure to HTML
    graph = fig.to_html(full_html=False)

    return render_template("index.html", data=data, graph=graph)


# Registration endpoint
@app.route("/register", methods=["POST"])
def register():
    first_name = request.json.get("first_name", None)
    last_name = request.json.get("last_name", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not all([email, password, first_name, last_name]):
        return jsonify({"msg": "Missing either email, password, first_name, or last_name"}), 400


    # Hash password
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    # Insert new user into database
    cur = conn.cursor()
    cur.execute("INSERT INTO users (email, password, first_name, last_name) VALUES (%s, %s, %s, %s)", (email, hashed_password, first_name, last_name))
    conn.commit()

    return jsonify({"msg": "User created successfully"}), 201

# Login endpoint
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    # Get user from database
    cur = conn.cursor()
    cur.execute("SELECT id, email, password FROM users WHERE email = %s", (email,))
    user = cur.fetchone()

    if not user:
        return jsonify({"msg": "Invalid email or password"}), 401

    # Check password
    if not bcrypt.check_password_hash(user[2], password):
        return jsonify({"msg": "Invalid email or password"}), 401

    # Extract id and email from user tuple
    user_id, user_email = user[0], user[1]

    # Create JWT access token with email as custom claim
    access_token = create_access_token(identity=user_id, additional_claims={"email": user_email})

    return jsonify({"access_token": access_token}), 200

# Protected endpoint
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    return jsonify({"user_id": user_id}), 200

if __name__ == "__main__":
    app.run(debug=True)
