from django.urls import URLPattern, path

from . import views

urlpatterns: list[URLPattern] = [
    path("profile", views.ProfileView.as_view(), name="my-profile"),
    path("profile/edit", views.ProfileEditView.as_view(), name="my-profile-edit"),
    path(
        "profile/onboarding", views.ProfileEditView.as_view(), name="profile-onboarding"
    ),
    path(
        "profile/settings", views.ProfileSettingsView.as_view(), name="profile-settings"
    ),
]
