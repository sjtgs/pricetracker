from google.cloud import vision
import re

def extract_text_from_image(image_path):
    """Extract text from an image using Google Vision API."""
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(f"Google Vision API error: {response.error.message}")

    # The first text annotation contains the full text detected
    full_text = texts[0].description if texts else ""

    # Extract specific details (name, description, price) using regex
    name = re.search(r"Name:\s*(.+)", full_text)
    description = re.search(r"Description:\s*(.+)", full_text)
    price = re.search(r"Price:\s*\$?([\d.]+)", full_text)

    return {
        "name": name.group(1) if name else "Unknown",
        "description": description.group(1) if description else "No description",
        "price": float(price.group(1)) if price else 0.0,
    }
