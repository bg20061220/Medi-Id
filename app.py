from flask import Flask, render_template, request, redirect, url_for
import os
from pill_identifier.ocr import extract_text_ocrspace
from pill_identifier.classifier import classify_pill
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load pill database


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'pill_image' not in request.files:
        return "No file uploaded", 400
    file = request.files['pill_image']
    if file.filename == '':
        return "Empty filename", 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Run OCR and Classification
    imprint = extract_text_ocrspace(filepath)
    prediction = classify_pill(filepath)

    # Find best match from pill_data
    best_match = None
    for pill in pill_data:
        if imprint and imprint.lower() in pill['imprint'].lower():
            best_match = pill
            break
        if prediction and prediction.lower() in pill['name'].lower():
            best_match = pill

    return render_template('result.html', image=file.filename, match=best_match)

if __name__ == '__main__':
    text, confidence = extract_text_ocrspace("pill_identifier/pill_database/watson853.jpeg")
    print("📦 Text:", text)
    print("📊 Confidence:", confidence)
    app.run(debug=True)
