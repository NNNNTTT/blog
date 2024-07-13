from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.article_view, name="article"),
    path("<int:pk>/", views.detail, name="detail"),
    path("create", views.create, name="create"),
    path("admin", views.admin, name="admin"),
    path("admin/<int:pk>/", views.edit, name="edit"),
    path("admin/update_or_delete/<int:pk>/", views.update_or_delete, name="update_or_delete"),
]