# DRF Imports
from django.urls import path

# View Imports
from .views import RoomsWishlistToggle, RoomsWishlists, RoomsWishlistDetail

urlpatterns = [
    path("", RoomsWishlists.as_view()),
    path("<int:pk>/", RoomsWishlistDetail.as_view()),
    path("<int:pk>/rooms/<int:room_pk>/", RoomsWishlistToggle.as_view()),
]
