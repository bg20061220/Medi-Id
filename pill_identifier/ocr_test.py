from ocr import extract_imprint  # Import your function from ocr.py

if __name__ == "__main__":
    # Path to your test image
    image_path = r"C:\Users\Admin\Documents\GitHub\Medi-Id\pill_identifier\test_pill.jpg"
        
    imprint_text = extract_imprint(image_path)
    print("Extracted Imprint Text:", imprint_text)
