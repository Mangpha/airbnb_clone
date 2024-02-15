# DRF Imports
from django.urls import path

# View Imports
from .views import Wishlists

urlpatterns = [
    path("", Wishlists.as_view()),
]
