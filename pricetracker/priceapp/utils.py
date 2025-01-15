# ocr_app/utils.py
from google.cloud import vision

def extract_text_from_image(image):
    """Extract text from an image using Google Vision API."""
    client = vision.ImageAnnotatorClient()
    content = image.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description  # First annotation contains all text
    return ""

def parse_text_to_items(text):
    """Parse the extracted text into structured items."""
    items = []
    lines = text.split("\n")
    for line in lines:
        if "K" in line:  # Check if the line contains a price
            parts = line.split("K")
            name = parts[0].strip()
            price = f"K{parts[1].strip()}"
            items.append({"name": name, "price": price, "description": ""})
    return items
