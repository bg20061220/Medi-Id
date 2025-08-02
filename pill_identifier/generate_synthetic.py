import cv2
import numpy as np
from ocr import extract_imprint  # Uses your existing OCR pipeline

# Create a blank white image
img = np.ones((100, 300), dtype=np.uint8) * 255

# Add clear, pill-style imprint text
cv2.putText(img, 'AB123', (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0), 3)

# Save to file
cv2.imwrite("synthetic_imprint.jpg", img)
print("✅ Synthetic image saved as synthetic_imprint.jpg")

# Run OCR on it
text = extract_imprint("synthetic_imprint.jpg")
print("🧾 Extracted from synthetic image:", text)
