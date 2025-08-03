# app.py

from flask import Flask, render_template, request , Blueprint , redirect, url_for, session , flash 
from werkzeug.utils import secure_filename
from .classifier import identify_pill
import os
from dotenv import load_dotenv
from auth.routes import MedicationSchedule
from auth.routes  import db

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
    total_pills = int(request.form["total_quantity"])
    pills_per_day = int(request.form["daily_dosage"])

    # Collect all 'dosage_time' fields (multiple with same name)
    dosage_times = request.form.getlist("dosage_time")

    if len(dosage_times) != pills_per_day:
        Warning("❗Mismatch between number of dosages and times entered.")
        return redirect(url_for("pill.schedule_form", medicine_name=med_name))

    for time in dosage_times:
        new_entry = MedicationSchedule(
            user_email=user_email,
            medicine_name=med_name,
            total_pills=total_pills,
            pills_per_day=pills_per_day,
            time_of_day=time  # One entry per time for now
        )
        db.session.add(new_entry)

    db.session.commit()
    Warning(f"✅ Scheduled {pills_per_day} doses for {med_name}")
    return redirect(url_for("pill.index"))

# if __name__ == "__main__":
#     app.run(debug=True)
