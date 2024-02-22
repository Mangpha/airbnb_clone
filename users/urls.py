# Django Imports
from django.urls import path

# DRF Imports
from rest_framework.authtoken.views import obtain_auth_token

# View Imports
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me/", views.Me.as_view()),
    path("change-password/", views.ChangePassword.as_view()),
    path("login/", views.Login.as_view()),
    path("logout/", views.Logout.as_view()),
    path("token-login", obtain_auth_token),
    path("jwt-login", views.JwtLogin.as_view()),
    path("@<str:username>/", views.PublicUser.as_view()),
]
