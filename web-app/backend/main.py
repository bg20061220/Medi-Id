from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# Create an app using Flask
app = Flask(__name__)
app.secret_key = "shhhsecret"

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///th25medipillaiusers.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

# User class
# User has an email and a hashed password which are both stored in the sqlite database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    # Set the password to the hashed value of the inputted password
    def setPassword(self, password):
        self.password = generate_password_hash(password)

    # Check whether the inputted password matches the account's actual password
    def checkPassword(self, inputted_password):
        return check_password_hash(self.password, inputted_password)


@app.route("/")
def home():
    if "email" in session:
        return redirect(url_for("homepage"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        exists = User.query.filter_by(email=email).first()
        if exists and exists.checkPassword(password):
            session["email"] = email
            return redirect(url_for("homepage"))
        else:
            flash('Invalid username or password. Please try again.', 'error')
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
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

@app.route("/homepage")
def homepage():
    if "email" in session:
        return render_template("homepage.html")
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect(url_for("homepage"))

if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    """
    with app.app_context():
        # Delete all rows from the User table
        User.query.delete()
        db.session.commit()
    print("Database has been cleared.")"""
    app.run(debug=True)
