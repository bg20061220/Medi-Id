# pill_matcher/match_pill.py

import os
import torch
import pickle
import numpy as np
from PIL import Image
from torchvision import models, transforms
from sklearn.metrics.pairwise import cosine_similarity

# Load precomputed embeddings
with open("pill_identifier/embeddings.pkl", "rb") as f:
    database = pickle.load(f)

# Load pretrained model (same as used in embedder.py)
model = models.resnet18(pretrained=True)
model = torch.nn.Sequential(*list(model.children())[:-1])
model.eval()

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def embed_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        vec = model(img_tensor).squeeze().numpy()
    return vec

def find_best_match(query_img_path, top_k=3):
    query_vec = embed_image(query_img_path)
    pill_names = list(database.keys())
    pill_vectors = np.array([database[name] for name in pill_names])
    
    similarities = cosine_similarity([query_vec], pill_vectors)[0]
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    results = [(pill_names[i], similarities[i]) for i in top_indices]
    return results

# 🧪 Test this
if __name__ == "__main__":
    test_image = "pill_identifier/test_pill.jpg"  # <- Replace with your test image
    results = find_best_match(test_image)
    
    print("🔍 Top Matches:")
    for name, score in results:
        print(f"{name} - Similarity: {score:.4f}")
