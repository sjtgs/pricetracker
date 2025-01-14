from django.urls import path 
from .views import pricescanner 

urlspatterns = [
    path("upload", pricescanner, name="pricescanner")
]