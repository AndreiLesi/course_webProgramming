from django.urls import path

from . import views

# app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("newPage", views.newPage, name="create"),
    path("edit/<str:title>", views.editPage, name="edit")
]