from dotenv import  load_dotenv
import os
import requests
from rapidfuzz import fuzz
load_dotenv()
import json 
API_KEY = os.getenv("ORC_SPACE_API_KEY")

def estimate_confidence(ocr_text, expected_text):
    """
    Returns a fuzzy match score between OCR output and expected name.
    Score is a percentage representing similarity between two strings.
    """
    if not ocr_text or not expected_text:
        return 0.0

    score = fuzz.ratio(ocr_text.lower(), expected_text.lower())
    return round(score, 2)


def extract_text_ocrspace(image_path, expected_text="v3601" ,  api_key=API_KEY):
    """
    Uses OCR.Space API to extract text from an image.
    Returns the extracted text and confidence (approximate).
    """
    url = "https://api.ocr.space/parse/image"
    payload = {
        'isOverlayRequired': False,
        'OCREngine': 2,  # Better engine
    }
    print("Expected text for confidence estimation:", expected_text)
    with open(image_path, 'rb') as f:
        files = {'file': f}
        if api_key:
            payload['apikey'] = api_key
        else:
            payload['apikey'] = api_key  # Public test key

        response = requests.post(url, files=files, data=payload)
        result = response.json()
        

    try:
        parsed = result["ParsedResults"][0]
        text = parsed["ParsedText"]
        confidence = estimate_confidence(text , expected_text)
        print(f"📦 OCR API text: {text.strip()}")
        print(f"📊 Confidence: {confidence:.2f}%")
        return text.strip(), confidence
    except Exception as e:
        print("❌ OCR API failed:", e)
        return "", 0.0

if __name__ == "__main__":
    image_path = "pill_identifier/pill_database/v3601.jpg"
    text, confidence = extract_text_ocrspace(image_path, api_key=API_KEY)