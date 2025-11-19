from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Profile
        fields = ["username", "email", "password1", "password2", "avatar", "bio"]

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    remember = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput())

