# ocr_app/views.py
import io
from django.shortcuts import render
from django.http import JsonResponse

from .forms import PriceScannerForm
from .models import Item
from .utils import extract_text_from_image, parse_text_to_items

def upload_image(request):
    if request.method == "POST":
        form = PriceScannerForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]

            # Use the utils to extract text and parse items
            text = extract_text_from_image(image)
            items = parse_text_to_items(text)

            # Save extracted items to the database
            for item_data in items:
                Item.objects.create(
                    name=item_data["name"],
                    price=item_data["price"],
                    description=item_data["description"],
                )

            return JsonResponse(items, safe=False)  # Return as JSON response

    else:
        form = PriceScannerForm()
    return render(request, "pricetacker/pricetracker.html", {"form": form})
