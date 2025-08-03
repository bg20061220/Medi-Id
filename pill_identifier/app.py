# app.py

from flask import Flask, render_template, request , Blueprint , redirect, url_for, session , flash 
from werkzeug.utils import secure_filename
from .classifier import identify_pill
import os
from dotenv import load_dotenv
from auth.routes import MedicationSchedule
from auth.routes  import db
from auth.routes import User

load_dotenv()
pill_bp = Blueprint('pill', __name__, template_folder='../templates')

# app = Flask(__name__)
# UPLOAD_FOLDER = os.path.join("static", "uploads")
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "..", "static", "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True) 
@pill_bp.route("/", methods=["GET", "POST"])

def index():
    result = None
    uploaded_file_path = None

    if request.method == "POST":
        file = request.files["image"]
        expected_name  = request.form.get("expected_name", "").strip()
        result = None
        uploaded_file_path = None
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            uploaded_file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(uploaded_file_path)

            # Run AI identification
            result = identify_pill(uploaded_file_path, expected_name)

    return render_template("index.html", result=result, image_path=uploaded_file_path)

@pill_bp.route("/schedule_form", methods=["GET"])
def schedule_form():
    if "email" not in session:
        return redirect(url_for("auth.login"))

    medicine_name = request.args.get("medicine_name", "")
    return render_template("schedule.html", medicine_name=medicine_name)
@pill_bp.route("/schedule", methods=["POST"])
def schedule_medicine():
    if "email" not in session:
        return redirect(url_for("auth.login"))

    user_email = session["email"]
    med_name = request.form.get("medicine_name")
    total_pills = int(request.form.get("total_quantity", 0))
    pills_per_day = int(request.form.get("daily_dosage", 0))

    dosage_times = request.form.getlist("dosage_time")

    if len(dosage_times) != pills_per_day:
        flash("❗Mismatch between number of dosages and times entered.", "error")
        return redirect(url_for("pill.schedule_form", medicine_name=med_name))

    user = User.query.filter_by(email=user_email).first()
    if not user:
        flash("User not found. Please log in again.", "error")
        return redirect(url_for("auth.login"))

    # Combine all dosage times as a CSV string
    time_of_day = ",".join(dosage_times)

    # Create one schedule entry per medicine per user
    new_schedule = MedicationSchedule(
        user_id=user.id,
        medicine_name=med_name,
        total_pills=total_pills,
        pills_per_day=pills_per_day,
        time_of_day=time_of_day
    )
    db.session.add(new_schedule)
    db.session.commit()

    flash(f"✅ Scheduled {pills_per_day} doses for {med_name}", "success")
    return redirect(url_for("pill.index"))


@pill_bp.route("/view_schedule" , methods=["GET"]) 
def view_schedule():
    if "email" not in session:
        return redirect(url_for("auth.login"))

    user = User.query.filter_by(email=session["email"]).first()
    if not user:
        return "User not found", 404

    # Get all schedules tied to the user's ID
    schedules = MedicationSchedule.query.filter_by(user_id=user.id).all()

    return render_template("view_schedule.html", schedules=schedules)
@pill_bp.route("/welcome", methods=["GET"])
def welcome():
    if "email" not in session:
        return redirect(url_for("auth.login"))

    user = User.query.filter_by(email=session["email"]).first()
    if not user:
        return "User not found", 404

    return render_template("welcome.html", user=user)
# if __name__ == "__main__":
#     app.run(debug=True)
