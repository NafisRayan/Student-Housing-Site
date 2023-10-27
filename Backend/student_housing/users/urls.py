from django.urls import path

from . import views

urlpatterns = [
    path("", views.users_intro, name="users_intro"),
]