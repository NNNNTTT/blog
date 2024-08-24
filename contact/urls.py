from django.contrib import admin
from django.urls import path
from .views import contact_view,contact_ok_view

app_name = "contact"
urlpatterns = [
    path("", contact_view, name="contact"),
    path("contact_ok/", contact_ok_view, name="contact_ok"),
]