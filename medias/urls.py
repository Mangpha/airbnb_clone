# Django Import
from django.urls import path

# View Import
from . import views

urlpatterns = [
    path("photos/get-url", views.GetUploadURL.as_view()),
    path("photos/<int:pk>", views.PhotoDetail.as_view()),
]
