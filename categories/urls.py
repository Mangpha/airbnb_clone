from django.urls import path
from . import views


urlpatterns = [
    path("", views.Categories.as_view()),
    path("<int:id>", views.CategoryDetail.as_view()),
]
