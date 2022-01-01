from django.urls import path

from . import views

app_name = "instruction"

urlpatterns = [
    path("", views.index, name="index"),
]