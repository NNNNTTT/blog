from django.contrib import admin
from django.urls import path, include
from . import views
app_name = "signup"

urlpatterns = [
    path("", views.index, name ="index"),
    path("signup/", views.signup_ok, name ="signup_ok"),
    path("username_create/", views.username_create, name ="username_create"),
    path("login/", views.login_view, name ="login"),
    path("logout/", views.logout_view, name ="logout"),
]