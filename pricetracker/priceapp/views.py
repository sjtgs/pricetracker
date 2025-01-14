from django.shortcuts import render
from django.http import JsonResponse
from .models import Item
from .forms import PriceScannerForm
from .utils import extract_text_from_image
import os

def pricescanner(request):
    if request.method == "POST":
        form = PriceScannerForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]
            image_path = f"temp/{image.name}"

            # Save the uploaded image temporarily
            os.makedirs("temp", exist_ok=True)
            with open(image_path, "wb") as f:
                for chunk in image.chunks():
                    f.write(chunk)

            # Extract text and process it
            data = extract_text_from_image(image_path)

            # Save to the database
            item = Item.objects.create(
                name=data["name"],
                description=data["description"],
                price=data["price"],
            )

            # Delete the temporary image
            os.remove(image_path)

            # Return JSON response
            return JsonResponse({
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "price": str(item.price),
            })
    else:
        form = PriceScannerForm()

    return render(request, "pricetracker_temp/pricetacker.html", {"form": form})
