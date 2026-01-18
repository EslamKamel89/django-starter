from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
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

    def post(self, request: HttpRequest):
        profile = request.user.profile  # type: ignore
        form = ProfileForm(instance=profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            profile = form.save()
            messages.success(request, "Your profile updated successfully")
            return redirect(reverse("my-profile"))
        messages.error(request, "Please fix the validation error")
        return render(request, "a_users/profile-edit.html", context={"form": form})
