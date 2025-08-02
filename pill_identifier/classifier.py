from pill_identifier.ocr import extract_text_ocrspace
from pill_identifier.match_pill import find_best_match

def identify_pill(image_path , expected_name , ocr_conf_treshold = 70):
    """
    Main logic to identify a pill based on an image.
    Returns a dictionary with both OCR and image match results.
    """
    print("🔍 Running OCR...")
    text , ocr_conf = extract_text_ocrspace(image_path , expected_name)

    print("🔍 Running Image Classification...")
    matches = find_best_match(image_path)
    top_match_label, top_match_score = matches[0] if matches else ("Unknown", 0.0)
    result = {
        "ocr_text": text, 
    "ocr_confidence": float(ocr_conf or 0.0),
        "image_matches": matches,
        "decision": ""
    }

    if ocr_conf >= 75:
        result["decision"] = f"🟢 High confidence. This looks like '{text}' and is likely safe to consume."
    elif ocr_conf >= 40:
        result["decision"] = f"🟡 Medium OCR confidence. Please verify before taking. OCR read: '{text}'"
    elif top_match_score >= 80:
        result["decision"] = f"🟡 OCR unclear, but image match suggests this may be '{top_match_label}' (Similarity: {top_match_score}%)"
    else:
        result["decision"] = "🔴 Low confidence from both OCR and image. DO NOT take without verification."

    
    return result 

if __name__ == "__main__":
    image_path = "pill_identifier/test_pill5.jpg"
    result = identify_pill(image_path)

    print("\n🎯 Final Decision:", result["decision"])
    print(f"📦 OCR Text: {result['ocr_text']} ({result['ocr_confidence']}%)")
    print("🔗 Top Image Matches:")
    for name, score in result["image_matches"]:
        print(f" - {name} (similarity: {score:.4f})")