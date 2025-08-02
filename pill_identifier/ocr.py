from dotenv import  load_dotenv
import os
import requests
load_dotenv()
import json 
API_KEY = os.getenv("ORC_SPACE_API_KEY")

def estimate_confidence(text):
    """
    Very basic confidence estimate:
    - Longer clean text = higher confidence
    - Short or junky OCR = lower confidence
    """
    clean_text = text.strip()
    if not clean_text:
        return 0.0
    if any(char.isalpha() for char in clean_text) and len(clean_text) >= 4:
        return 90.0  # Assume high if readable alphanumeric
    if len(clean_text) <= 2:
        return 30.0
    return 50.0


def extract_text_ocrspace(image_path, api_key=API_KEY):
    """
    Uses OCR.Space API to extract text from an image.
    Returns the extracted text and confidence (approximate).
    """
    url = "https://api.ocr.space/parse/image"
    payload = {
        'isOverlayRequired': False,
        'OCREngine': 2,  # Better engine
    }

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
        confidence = estimate_confidence(text)
        print(f"📦 OCR API text: {text.strip()}")
        print(f"📊 Confidence: {confidence:.2f}%")
        return text.strip(), confidence
    except Exception as e:
        print("❌ OCR API failed:", e)
        return "", 0.0

if __name__ == "__main__":
    image_path = "pill_identifier/pill_database/v3601.jpg"
    text, confidence = extract_text_ocrspace(image_path, api_key=API_KEY)