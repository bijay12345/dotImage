from django.urls import path
from . import views

urlpatterns = [
    path("", views.ArtView.as_view(), name="uploadImage"),
]