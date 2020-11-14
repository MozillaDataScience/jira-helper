from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<issue_key>", views.detail, name="detail"),
]
