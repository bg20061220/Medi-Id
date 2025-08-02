# app.py

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from pill_identifier.classifier import identify_pill
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    uploaded_file_path = None

    if request.method == "POST":
        file = request.files["image"]
        expected_name  = request.form.get("expected_name", "").strip()
        if file:
            filename = secure_filename(file.filename)
            uploaded_file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(uploaded_file_path)

            # Run AI identification
            result = identify_pill(uploaded_file_path , expected_name)

    return render_template("index.html", result=result, image_path=uploaded_file_path)

if __name__ == "__main__":
    app.run(debug=True)
