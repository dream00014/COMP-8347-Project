from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

from .models import UserProfile, PaymentMethod

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'date_of_birth', 'gender', 'address', 'city', 'province', 'postal_code', 'country', 'phone_number']

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class PasswordChangeForm(PasswordChangeForm):
    # You can customize this form if needed
    pass

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['method_type', 'account_number', 'is_default']
