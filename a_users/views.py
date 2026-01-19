from allauth.account.models import EmailAddress
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from a_users.forms import EmailForm, ProfileForm


class ProfileView(View):
    def get(self, request: HttpRequest, username: str | None = None):
        if username:
            profile = get_object_or_404(User, username=username).profile  # type: ignore
        else:
            try:
                profile = request.user.profile  # type: ignore
            except:
                return redirect(reverse("account_login"))
        return render(request, "a_users/profile.html", context={"profile": profile})


class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        profile = request.user.profile  # type: ignore
        form = ProfileForm(instance=profile)
        if request.path == reverse("profile-onboarding"):
            onboarding = True
        else:
            onboarding = False
        return render(
            request,
            "a_users/profile-edit.html",
            context={"form": form, "onboarding": onboarding},
        )

    def post(self, request: HttpRequest):
        profile = request.user.profile  # type: ignore
        form = ProfileForm(instance=profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            profile = form.save()
            messages.success(request, "Your profile updated successfully")
            return redirect(reverse("my-profile"))
        messages.error(request, "Please fix the validation error")
        return render(request, "a_users/profile-edit.html", context={"form": form})


class ProfileSettingsView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        return render(request, "a_users/profile-settings.html")


class EmailChangeView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        if request.htmx:  # type: ignore
            form = EmailForm(instance=request.user)  # type: ignore
            return render(request, "a_users/partials/email-form.html", {"form": form})
        return redirect(reverse("home"))

    def post(self, request: HttpRequest):
        form = EmailForm(instance=request.user, data=request.POST)  # type: ignore
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if email == request.user.email:  # type: ignore
                messages.info(request, "This is already your current email address")
                return redirect(reverse("profile-settings"))
            if EmailAddress.objects.filter(email=email).exclude(id=request.user.id).exists():  # type: ignore
                messages.warning(request, "Email is already in use")
                return redirect(reverse("profile-settings"))
            form.save()
            email_address = EmailAddress.objects.filter(
                user=request.user,
                email=email,
                primary=True,
            ).first()
            if email_address:
                email_address.send_confirmation(request)
            messages.success(
                request, "Email updated. Please check your inbox to verify it."
            )
            return redirect(reverse("profile-settings"))
        messages.error(request, "Please fix the validation error")
        return render(request, "a_users/partials/email-form.html", {"form": form})
