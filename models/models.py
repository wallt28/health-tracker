from flask_sqlalchemy import SQLAlchemy

from db import db

# Define the 'users' table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

# Define the table to track health and fitness metrics
class HealthMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    sleep = db.Column(db.Integer, nullable=True)
    calories = db.Column(db.Integer, nullable=True)
    step_count = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    bodyfat = db.Column(db.Float, nullable=True)
    mood = db.Column(db.String(20), nullable=True)
    protein = db.Column(db.Float, nullable=True)
    carbs = db.Column(db.Float, nullable=True)
    fats = db.Column(db.Float, nullable=True)
