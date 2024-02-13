# Django Import
from django.urls import path

# View Import
from .views import PhotoDetail

urlpatterns = [
    path("photos/<int:pk>", PhotoDetail.as_view()),
]
