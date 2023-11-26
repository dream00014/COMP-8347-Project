from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import CryptoCurrency, Score, Customer
import os
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

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


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    id_document = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), validators=[validate_file_extension], required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])

        # 需要决定如何获取这些值
        first_name = "Default"  # 可以从表单获取或设置默认值
        last_name = "Default"  # 可以从表单获取或设置默认值
        head_photo = None  # 可以从表单获取或设置默认值
        email_address = self.cleaned_data.get("email", "")

        if commit:
            user.save()
            Customer.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                head_photo=head_photo,
                email_address=email_address
            )

        return user


# Yang Wang's forms

class SpotSearchForm(forms.Form):
    keyword = forms.CharField(max_length=100, required=False, label='Search for companies')

    min_score = forms.IntegerField(required=False, label='Min Score')
    max_score = forms.IntegerField(required=False, label='Max Score')

    # min_volume = forms.IntegerField(required=False, label='Min Volume')
    # max_volume = forms.IntegerField(required=False, label='Max Volume')
    #
    # min_liquidity = forms.IntegerField(required=False, label='Min Liquidity')
    # max_liquidity = forms.IntegerField(required=False, label='Max Liquidity')
    #
    # min_weekly_visit = forms.IntegerField(required=False, label='Min Weekly Visit')
    # max_weekly_visit = forms.IntegerField(required=False, label='Max Weekly Visit')
    #
    # min_markets = forms.IntegerField(required=False, label='Min Markets')
    # max_markets = forms.IntegerField(required=False, label='Max Markets')
    #
    # min_coins = forms.IntegerField(required=False, label='Min Coins')
    # max_coins = forms.IntegerField(required=False, label='Max Coins')


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['score']
        labels = {
            'score': 'Your Score'
        }
        widgets = {
            'score': forms.Select(choices=Score.score_choice)
        }
