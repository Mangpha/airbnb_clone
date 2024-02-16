# Django Imports
from django.urls import path

# View Imports
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me/", views.Me.as_view()),
]
