from django.urls import path

from . import views

urlpatterns = [
    path("", views.users_intro, name="users_intro"),
    path("login/", views.users_login, name="users_login"),
    path("register/", views.users_register, name="users_register"),
]