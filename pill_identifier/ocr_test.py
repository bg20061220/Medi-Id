from ocr import extract_imprint

# Replace with your actual test image path
image_path = "pill_identifier/test_pill3.jpg"

imprint = extract_imprint(image_path)
print("🧾 Extracted Imprint Text:", imprint)

