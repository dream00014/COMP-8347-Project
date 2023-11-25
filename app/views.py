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
from .forms import CryptoSelectionForm
from .models import CryptoCurrency
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import HttpResponseRedirect



class PortfolioView(LoginRequiredMixin,View):
    login_url = "/login"

    def get(self, request):
        print(request.user)
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


class ExchangeView(LoginRequiredMixin,View):
    login_url = "/login"

    def get(self, request, selected_crypto=None):
        if not selected_crypto:
            error = {"error": "selected_crypto or selected_fiat is None"}
            return JsonResponse(error, safe=False)

        crypto_data = CryptoCurrency.objects.all()
        fiat_data = FiatCurrency.objects.all()
        print(selected_crypto, "=========>>>>>>")
        selected_crypto = CryptoCurrency.objects.filter(symbol=selected_crypto).first()
        print(selected_crypto, "-----------")
        context = {
            "crypto_data": crypto_data,
            "fiat_data": fiat_data,
            "selected_crypto": selected_crypto,
            "selected_value": {"crypto": selected_crypto},
        }
        return render(request, "exchange.html", context=context)


class GetExchangePrice(LoginRequiredMixin,View):
    login_url = "/login"

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

            print(username, password)
            user = authenticate(username=username, password=password)

            print("USER===========", user)
            if user:
                login(request, user)
                return redirect("portfolio_view")
            else:
                # Add the form to the context if login fails
                context = {"form": form}
                return render(request, "login.html", context=context)

        # If the form is not valid, render the form with errors
        context = {"form": form}
        return render(request, "login.html", context=context)


class SignUpView(View):
    def get(self, request):
        form = SignUpForm(request.GET)

        context = {"form": form}
        return render(request, "signup.html", context=context)

    def post(self, request):
        form = SignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            hash_password = make_password(password)
            print(username, hash_password)
            user = User(username=username, password=hash_password)
            user.save()
            return redirect("portfolio_view")

        # If the form is not valid, render the form with errors
        context = {"form": form}
        return render(request, "signup.html", context=context)


class LogoutView(LoginRequiredMixin, View):
    login_url = "/login"

    def get(self, request):
        print(request.user, "========1")
        logout(request)
        print(request.user, "=======2")
        return redirect("login_view")


def logoutView():
    return {'abc':'bbc'}


class CryptoSelectionView(View):
    def get(self, request):
        form = CryptoSelectionForm()
        return render(request, 'crypto_selection.html', {'form': form})

    def post(self, request):
        form = CryptoSelectionForm(request.POST)
        if form.is_valid():
            crypto_id = form.cleaned_data['crypto']
            selected_crypto = CryptoCurrency.objects.get(id=crypto_id)
            return render(request, 'crypto_details.html', {'form': form, 'selected_crypto': selected_crypto})
        return render(request, 'crypto_selection.html', {'form': form})

stripe.api_key = settings.STRIPE_SECRET_KEY

#existing payment view
class PaymentView(View):
    def post(self, request):
        intent = stripe.PaymentIntent.create(
            amount= int(float(request.POST['total_price'])),
            currency='usd',
            automatic_payment_methods={
                'enabled': True,
            },
        )

        #store data into temp transactions table
        print(intent['client_secret'])

        return render(request, 'payment.html', {'form': intent['client_secret'], 'crypto_type' : request.POST['crypto'], 'crypto_qty' : request.POST['quantity']})




class checkoutSuccess(View):
    def get(self, request):
        return render(request, 'checkout.html')
