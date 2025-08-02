from ocr import extract_text_ocrspace
from match_pill import find_best_match

def identify_pill(image_path , ocr_conf_treshold = 70):
    """
    Main logic to identify a pill based on an image.
    Returns a dictionary with both OCR and image match results.
    """
    print("🔍 Running OCR...")
    text , ocr_conf = extract_text_ocrspace(image_path)

    print("🔍 Running Image Classification...")
    matches = find_best_match(image_path)

    result = {
        "ocr_text": text, 
        "ocr_confidence": ocr_conf,
        "image_matches": matches,
        "decision": ""
    }

    if ocr_conf >= ocr_conf_treshold:
        result["decision"] = f"🟢 High confidence in OCR: '{text}'"
    elif ocr_conf >=40 :
                result["decision"] = f"🟡 Uncertain OCR, showing top image match: '{matches[0][0]}'"
    else:
        result["decision"] = "🔴 Low confidence in OCR, relying on image matches."
    
    return result 

if __name__ == "__main__":
    image_path = "pill_identifier/test_pill5.jpg"
    result = identify_pill(image_path)

    print("\n🎯 Final Decision:", result["decision"])
    print(f"📦 OCR Text: {result['ocr_text']} ({result['ocr_confidence']}%)")
    print("🔗 Top Image Matches:")
    for name, score in result["image_matches"]:
        print(f" - {name} (similarity: {score:.4f})")