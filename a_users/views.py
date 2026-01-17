from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


class ProfileView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        return render(request, "a_users/profile.html")
