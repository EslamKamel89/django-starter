from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from a_users.forms import ProfileForm


class ProfileView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        profile = request.user.profile  # type: ignore
        return render(request, "a_users/profile.html", context={"profile": profile})


class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        profile = request.user.profile  # type: ignore
        form = ProfileForm(instance=profile)
        return render(request, "a_users/profile-edit.html", context={"form": form})
