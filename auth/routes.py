# auth/routes.py

from flask import Blueprint, render_template, request, redirect, session, url_for, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import date 
auth_bp = Blueprint('auth', __name__, template_folder='../templates')

db = SQLAlchemy()  # We'll initialize this in the main app

# User model needs to be accessible here too
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    def setPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, inputted_password):
        return check_password_hash(self.password, inputted_password)
    schedules = db.relationship('MedicationSchedule', backref='user', lazy=True , foreign_keys='MedicationSchedule.user_id')


class MedicationSchedule(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String, nullable=False)
    medicine_name = db.Column(db.String, nullable=False)
    total_pills = db.Column(db.Integer, nullable=False)
    pills_per_day = db.Column(db.Integer, nullable=False)
    time_of_day = db.Column(db.String, nullable=False)  # e.g. "08:00, 20:00"
    start_date = db.Column(db.Date, nullable=False, default=date.today)
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # ✅ this is critical

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        exists = User.query.filter_by(email=email).first()
        if exists and exists.checkPassword(password):
            session["email"] = email
            return redirect(url_for("pill.index"))  # Adjusted for pill blueprint homepage route
        else:
            flash('Invalid username or password. Please try again.', 'error')
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        exists = User.query.filter_by(email=email).first()

        if exists:
            flash('Email has already been used.', 'error')
            return render_template("register.html")

        elif password != confirmPassword:
            flash('Passwords do not match.', 'error')
            return render_template("register.html")

        elif not exists and password == confirmPassword:
            user = User(email=email)
            user.setPassword(password)
            db.session.add(user)
            db.session.commit()
            flash('Your account was successfully created! Sign into your account on the login page here.')
            return render_template("login.html")

    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.pop("email", None)
    return redirect(url_for("auth.login"))
