# pill_matcher/embedder.py

import os
import torch
import pickle
from torchvision import models, transforms
from PIL import Image

# Path to your pill images
IMAGE_DIR = "pill_identifier/pill_database"
OUTPUT_FILE = "pill_identifier/embeddings.pkl"

# Load pretrained ResNet18
model = models.resnet18(pretrained=True)
model = torch.nn.Sequential(*list(model.children())[:-1])  # Remove classification layer
model.eval()

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Embed all images
embeddings = {}
for file in os.listdir(IMAGE_DIR):
    if file.lower().endswith((".jpg", ".png",".jpeg")):
        path = os.path.join(IMAGE_DIR, file)
        img = Image.open(path).convert("RGB")
        img_tensor = transform(img).unsqueeze(0)
        with torch.no_grad():
            vec = model(img_tensor).squeeze().numpy()
            embeddings[file] = vec

# Save to pickle
with open(OUTPUT_FILE, "wb") as f:
    pickle.dump(embeddings, f)

print(f"✅ Embedded {len(embeddings)} pills to {OUTPUT_FILE}")
