from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import CryptoCurrency
import os

# Custom validator for file upload
def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png', '.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed types are .jpg, .png, .pdf')

class RankingFilterForm(forms.Form):
    RANKING_CHOICES = [
        ("all", "All Rankings"),
        ("top", "Top Rankings"),
        ("worst", "Worst Rankings"),
    ]

    ranking_filter = forms.ChoiceField(
        choices=RANKING_CHOICES,
        label="Filter by Ranking",
        widget=forms.Select(attrs={"class": "form-control"}),
        initial="all",
    )

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )

class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )
    confirm_password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm Password"}),
    )
    id_document = forms.FileField(
        required=True,
        validators=[validate_file_extension],
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Confirm Password does not match Password.")

        return cleaned_data

class CryptoSelectionForm(forms.Form):
    crypto_choices = [(crypto.id, crypto.name) for crypto in CryptoCurrency.objects.all()]
    crypto = forms.ChoiceField(choices=crypto_choices, widget=forms.Select(attrs={'class': 'form-select'}))
