from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


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
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )


class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )

    confirm_password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if not len(username) > 0:
            print("\n\n ERROR: Username not be blank.\n\n")
            raise ValidationError("Username not be blank.")

        if not len(password) > 0:
            print("\n\n ERROR: Password not be blank.\n\n")

            raise ValidationError("Password not be blank.")

        if not len(confirm_password) > 0:
            print("\n\n ERROR: Confirm Password not be blank.\n\n")
            raise ValidationError("Confirm Password not be blank.")

        if password != confirm_password:
            print("\n\n ERROR: Confirm Password not matched with Password.\n\n")
            raise ValidationError("Confirm Password not matched with Password.")

        return cleaned_data
