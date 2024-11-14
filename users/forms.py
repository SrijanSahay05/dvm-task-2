from django import forms
from .models import CustomUser, PassengerProfile, RailwayStaffProfile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]


class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "password"]
