from django.urls import path
from . import views


urlpatterns = [
    path("", views.categories),
    path("<int:id>", views.category),
]
