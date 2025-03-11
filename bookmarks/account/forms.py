from django import forms

class LogingForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)