from django.urls import URLPattern, path

from . import views

urlpatterns: list[URLPattern] = [
    path("profile", views.ProfileView.as_view(), name="my-profile")
]
