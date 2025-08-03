from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from auth.routes import auth_bp, db
from pill_identifier.app import pill_bp
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///th25medipillaiusers.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(pill_bp, url_prefix='/')

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    
    
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)