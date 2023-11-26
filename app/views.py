from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.views import View
from django.forms.models import model_to_dict
import requests
from .forms import RankingFilterForm, LoginForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from .models import CryptoCurrency
import json
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .forms import *



from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class PortfolioView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        filter_by = request.GET.get("ranking_filter")
        form = RankingFilterForm(request.GET)

        if filter_by == "top":
            data = CurrencyExchangeInfo.objects.filter(
                fiat_currency__symbol="USD"
            ).order_by("price")[:10]
        elif filter_by == "worst":
            data = CurrencyExchangeInfo.objects.filter(
                fiat_currency__symbol="USD"
            ).order_by("-price")[:10]
        else:
            data = CurrencyExchangeInfo.objects.filter(fiat_currency__symbol="USD")

        context = {"form": form, "data": data}

        return render(request, "portfolio.html", context=context)


class ExchangeView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, selected_crypto=None, action=None):
        if not selected_crypto:
            error = {"error": "selected_crypto or selected_fiat is None"}
            return JsonResponse(error, safe=False)

        if not action:
            error = {"error": "action[BUY or SELL] is None"}
            return JsonResponse(error, safe=False)

        crypto_data = CryptoCurrency.objects.all()
        fiat_data = FiatCurrency.objects.all()
        selected_crypto = CryptoCurrency.objects.filter(symbol=selected_crypto).first()
        context = {
            "crypto_data": crypto_data,
            "fiat_data": fiat_data,
            "selected_crypto": selected_crypto,
            "selected_value": {"crypto": selected_crypto},
            "action": action,
        }

        return render(request, "exchange.html", context=context)


class GetExchangePrice(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, crypto_symbol, fiat_symbol):
        data = CurrencyExchangeInfo.objects.filter(
            crypto_currency__symbol=crypto_symbol, fiat_currency__symbol=fiat_symbol
        ).first()

        obj_dict = model_to_dict(data)

        return JsonResponse(obj_dict, safe=False)


class LoginView(View):
    def get(self, request):
        form = LoginForm(request.GET)

        context = {"form": form}
        return render(request, "login.html", context=context)

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("portfolio_view")
            else:
                context = {"form": form}
                return render(request, "login.html", context=context)

        context = {"form": form}
        return render(request, "login.html", context=context)


class LogoutView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        logout(request)
        return redirect("login_view")


class TransactionView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        data = request.GET.get("data", "")
        unescaped_string = data.encode().decode("unicode_escape")
        data_dict = json.loads(unescaped_string)

        try:
            try:
                user_obj = CustomUser.objects.get(username=data_dict["user"])
            except Exception as e:
                data = {"msg": "Transaction Failed", "error": e}
                return JsonResponse(data)
            transaction = TransactionHistory(
                user=user_obj,
                transaction_type=data_dict["transaction_type"],
                transaction_status=data_dict["transaction_status"],
                from_currency=data_dict["from_currency"],
                from_currency_qty=data_dict["from_currency_qty"],
                to_currency=data_dict["to_currency"],
                to_currency_amount=data_dict["to_currency_amount"],
                total_amount=data_dict["total_amount"],
            )

            transaction.save()

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            raise ValidationError(f"Error decoding JSON: {e}")

        return redirect("/")


class TransactionHistoryView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        transaction_histories = TransactionHistory.objects.filter(
            user__pk=request.user.pk
        ).all()
        context = {"transaction_histories": transaction_histories}
        return render(request, "transaction_history.html", context=context)


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect("login_view")
        else:
            return render(request, "signup.html", {"form": form})


class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = "user_dashboard.html"
    success_url = reverse_lazy("profile_view")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "profile_edit.html"
    success_url = reverse_lazy("profile_view")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
