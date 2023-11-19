from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, UserUpdateForm, PasswordChangeForm, PaymentMethodForm
from django.contrib import messages

from .models import UserProfile, PaymentMethod, PaymentHistory


@login_required
def user_settings(request):
    user_profile = UserProfile.objects.get(user=request.user)
    payment_methods = PaymentMethod.objects.filter(user=request.user)
    payment_history = PaymentHistory.objects.filter(user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('user_settings')

        if password_form.is_valid():
            password_form.save()
            messages.success(request, 'Your password has been updated!')
            return redirect('user_settings')

    else:
        profile_form = UserProfileForm(instance=user_profile)
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    payment_method_form = PaymentMethodForm()

    return render(request, 'user_settings.html', {
        'profile_form': profile_form,
        'user_form': user_form,
        'password_form': password_form,
        'payment_methods': payment_methods,
        'payment_history': payment_history,
        'payment_method_form': payment_method_form,
    })
