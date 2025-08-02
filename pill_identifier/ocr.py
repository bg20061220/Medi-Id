import pytesseract
import cv2

# If on Windows and Tesseract not in PATH, uncomment & update the line below:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_imprint(image_path):
    """
    Extracts text (imprint) from a pill image using OCR.
    Applies some preprocessing for better accuracy.
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not load image at {image_path}")
            return None
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.adaptiveThreshold(
            blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2
        )
        text = pytesseract.image_to_string(thresh)
        print("OCR text detected:", text)
        return text.strip()
    except Exception as e:
        print("OCR error:", e)
        return None
