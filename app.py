from flask import Flask, render_template, request, jsonify, redirect, make_response, url_for, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    decode_token
)
from forms import LoginForm, RegistrationForm
from flask_bcrypt import Bcrypt
import plotly.graph_objs as go
import dotenv
import jwt

from plotly.subplots import make_subplots
from models import User, HealthMetric

from db import db


# ? To do next: Create a log output that allows users to delete & update entries easily


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this in production
app.config["SECRET_KEY"] = "your-secret-key-here"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mypassword@db/healthtracker'
db.init_app(app)


with app.app_context():
    db.create_all()

jwt = JWTManager(app)
bcrypt = Bcrypt(app)


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/home2", methods=["GET"])
def home2():
    return render_template("home_2.html")



@app.route("/workouts", methods=["GET", "POST"])
def workouts():
    return render_template("workouts.html")


#! ADD LOGIC SO THAT IF USER DATA ISNT THERE,
#! DISPLAY ON HTML "NO DATA HAS BEEN ADDED, TRY ADDING SOME OR CLICK HERE TO ADD"

# Display the health metric logs for a user
@app.route('/health_metric_logs/<int:user_id>', methods=["GET", "POST"])
def health_metric_logs(user_id):
    # Get the health metric logs for the specified user
    health_metrics = HealthMetric.query.filter_by(user_id=user_id).all()
    print(user_id)
    print(health_metrics)

    return render_template('health_metric_logs.html', health_metrics=health_metrics)

# Delete a health metric log entry
@app.route('/delete_health_metric/<int:id>', methods=["GET", "POST"])
def delete_health_metric(id):
    # Find the health metric log entry with the specified ID
    health_metric = HealthMetric.query.get(id)

    if health_metric:
        # Delete the health metric log entry from the database
        db.session.delete(health_metric)
        db.session.commit()

    return redirect(url_for('health_metric_logs', user_id=health_metric.user_id))


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    #! Change to JWT / more secure in the future
    try:
        access_token = request.cookies.get("access_token")
        decoded_token = decode_token(access_token)

    except:
        return jsonify("No access token - functionality to follow - please go to LOGIN.")

    user_id = decoded_token["user_id"]

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
        try:
            metric = HealthMetric.query.filter_by(date=date, user_id=user_id).one()
            metric.calories = calories
            metric.protein = protein
            metric.carbs = carbs
            metric.fats = fats
            metric.sleep = sleep
            metric.mood = mood
        except NoResultFound:
            # Add new entry to database
            metric = HealthMetric(date=date, calories=calories, protein=protein, carbs=carbs, fats=fats, sleep=sleep, mood=mood, user_id=user_id)
            db.session.add(metric)

        db.session.commit()

    # Fetch data from database
    data = []
    for metric in HealthMetric.query.filter_by(user_id=user_id).order_by(HealthMetric.date.desc()):
        data.append({
            "date": metric.date,
            "calories": metric.calories,
            "protein": metric.protein,
            "carbs": metric.carbs,
            "fats": metric.fats,
            "sleep": metric.sleep,
            "mood": metric.mood,
        })

    # Calculate averages
    num_metrics = len(data)
    if num_metrics > 0:
        avg_calories = sum(metric["calories"] for metric in data) / num_metrics
        avg_protein = sum(metric["protein"] for metric in data) / num_metrics
        avg_carbs = sum(metric["carbs"] for metric in data) / num_metrics
        avg_fats = sum(metric["fats"] for metric in data) / num_metrics
        avg_sleep = sum(metric["sleep"] for metric in data) / num_metrics
        total_mood = sum(int(metric["mood"]) for metric in data)
        avg_mood = total_mood / num_metrics
    else:
        avg_calories = 0
        avg_protein = 0
        avg_carbs = 0
        avg_fats = 0
        avg_sleep = 0
        avg_mood = 0

    avg_metrics = {
        "calories": round(avg_calories),
        "protein": round(avg_protein),
        "carbs": round(avg_carbs),
        "fats": round(avg_fats),
        "sleep": round(avg_sleep),
        "mood": round(avg_mood),
    }


    # Create plotly figure
    fig = make_subplots(
        rows=2,
        cols=3,
        subplot_titles=("Calories", "Sleep", "Mood", "Fats", "Protein", "Carbs"),
    )
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
    fig.update_layout(height=600, title_text="Nutrition")
    #fig2.update_layout(height=600, title_text="Body Composition")
    #fig3.update_layout(height=600, title_text="Well-being")
    #fig4.update_layout(height=600, title_text="Physical Activity")

    # Convert plotly figure to HTML
    graphData = fig.to_html(full_html=False)


    access_token = request.cookies.get("access_token")






    if access_token:
        decoded_token = decode_token(access_token)
        name = decoded_token['name'].title()
        first_name = (f"{name}'s")
    else:
        first_name = "Your"

    return render_template("dashboard.html", data=data, avg_metrics=avg_metrics, graph=graphData, first_name=first_name)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return jsonify({"msg": "Missing email or password"}), 400

        # Get user from database
        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"msg": "Invalid email or password"}), 401

        # Check password
        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({"msg": "Invalid email or password"}), 401

        # Extract id and email from user object
        user_id, user_email, first_name = user.id, user.email, user.first_name

        # Create JWT access token with email as custom claim
        access_token = create_access_token(
            identity=user_id,
            additional_claims={"email": user_email, "name": first_name, "user_id": user_id},
        )

        print()

        # Store JWT in a cookie
        response = make_response(redirect("/dashboard"))
        response.set_cookie("access_token", access_token)

        return response

    form = LoginForm()
    return render_template("login.html", form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    print("test print")
    if request.method == 'POST':
        print("test print")
        first_name = request.form.get("first_name", None)
        last_name = request.form.get("last_name", None)
        email = request.form.get("email", None)
        password = request.form.get("password", None)
        print(first_name, last_name, email, password)

        if not all([email, password, first_name, last_name]):
            return (
                jsonify(
                    {"msg": "Missing either email, password, first_name, or last_name"}
                ),
                400,
            )

        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Insert new user into database
        new_user = User(email=email, password=hashed_password, first_name=first_name, last_name=last_name)

        try:
            db.session.add(new_user)

            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return (jsonify({"msg": "Email already exists."}), 409)


        return redirect(url_for('login'))

    form = RegistrationForm()

    return render_template('register.html', form=form)

# Login endpoint




if __name__ == "__main__":
    app.run(debug=True)