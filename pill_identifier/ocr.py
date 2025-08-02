import cv2
import pytesseract
import numpy as np

# Tesseract path (update if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_imprint(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ Error: Could not load image at {image_path}")
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    gray_enhanced = clahe.apply(gray)

    edges = cv2.Canny(gray_enhanced, 100, 200)
    kernel = np.ones((3,3), np.uint8)
    edges_dilated = cv2.dilate(edges, kernel, iterations=1)

    combined = cv2.bitwise_or(gray_enhanced, edges_dilated)

    thresh = cv2.adaptiveThreshold(
        combined, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered = [c for c in contours if cv2.contourArea(c) > 30]

    if not filtered:
        print("⚠️ No usable contours found. OCR on full image.")
        processed_img = thresh
    else:
        x_min, y_min, x_max, y_max = img.shape[1], img.shape[0], 0, 0
        for cnt in filtered:
            x, y, w, h = cv2.boundingRect(cnt)
            x_min = min(x_min, x)
            y_min = min(y_min, y)
            x_max = max(x_max, x + w)
            y_max = max(y_max, y + h)

        processed_img = gray[y_min:y_max, x_min:x_max]

    processed_img = cv2.resize(processed_img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

    sharpen_kernel = np.array([[0, -1, 0],
                               [-1, 5, -1],
                               [0, -1, 0]])
    processed_img = cv2.filter2D(processed_img, -1, sharpen_kernel)

    cv2.imwrite("debug_processed.jpg", processed_img)
    print("🖼️ Saved processed image as debug_processed.jpg")

    config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    text = pytesseract.image_to_string(processed_img, config=config)

    print("📦 OCR text detected:", text)
    return text.strip()

