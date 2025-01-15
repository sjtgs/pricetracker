from django.urls import path 
from .views import pricescanner 

urlpatterns = [
    path("upload", pricescanner, name="pricescanner")
]