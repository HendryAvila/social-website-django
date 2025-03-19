from django import forms
from django.contrib.auth.models import User
from . import models
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class LogingForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Repite tu contraseña",
        widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Las contraseñas no coincident")
        else:
            return cd["password2"]
    
    def clean_email(self) -> None:
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            logging.error("El email ya esta siendo utilizado")
            raise forms.ValidationError("El email ya esta siendo utilizado")


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
    
    def clean_email(self):
        data = self.cleaned_data["email"]
        queryset = User.objects.exclude(id=self.instance.id).filter(email=data)

        if queryset.exists():
            logging.error("El email ya se encuentra en uso")
            raise forms.ValidationError("El email ya se encuentra en uso")
        return data

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ["date_of_birth", "photo"]
    