from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal

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
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class PortfolioView(LoginRequiredMixin, View):
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


class ExchangeView(LoginRequiredMixin, View):
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


class GetExchangePrice(LoginRequiredMixin, View):
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


class LogoutView(LoginRequiredMixin, View):
    login_url = "/login"

    def get(self, request):
        print(request.user, "========1")
        logout(request)
        print(request.user, "=======2")
        return redirect("login_view")


def logoutView():
    return {'abc': 'bbc'}


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


# existing payment view
class PaymentView(View):
    def post(self, request):
        paymentObj = stripe.PaymentIntent.create(
            amount=int(float(request.POST['total_price'])),
            currency=request.POST['fiat'].lower(),
            automatic_payment_methods={
                'enabled': True,
            },
        )

        new_transaction = Transaction.objects.create(
            user=User.objects.get(id=request.user.id),
            secret_key=paymentObj['client_secret'],
            crypto_currency=CryptoCurrency.objects.get(symbol=request.POST['crypto']),
            crypto_amount=float(request.POST['quantity']),
            amount_paid=float(request.POST['total_price']),
            amount_currency=FiatCurrency.objects.get(symbol=request.POST['fiat']),
            date_time=datetime.now(),
            transactions_type=True,
            status=False
        )

        new_transaction.save()

        return render(request, 'payment.html',
                      {'form': paymentObj['client_secret'], 'crypto_type': request.POST['crypto'],
                       'crypto_qty': request.POST['quantity']})


# existing payment view
class SellView(View):
    def post(self, request):
        msgToRtrn = ""

        crypto_amount_paid_ = float(request.POST['quantity'])
        cryptoCurrency = CryptoCurrency.objects.get(symbol=request.POST['crypto'])
        all_transactions = Transaction.objects.filter(user=request.user.id, crypto_currency=cryptoCurrency.id)
        transSum = 0
        for transaction in all_transactions:
            transSum += transaction.crypto_amount

        if crypto_amount_paid_ <= transSum:
            sell_transaction = ForexTransaction.objects.create(
                user=User.objects.get(id=request.user.id),
                crypto_currency=cryptoCurrency,
                crypto_amount_paid=crypto_amount_paid_,
                currency_amount_purchased=float(request.POST['total_price']),
                forex_currency=FiatCurrency.objects.get(symbol=request.POST['fiat']),
                date_time=datetime.now(),
                status=True
            )

            sell_transaction.save()

            new_transaction = Transaction.objects.create(
                user=User.objects.get(id=request.user.id),
                secret_key='',
                crypto_currency=CryptoCurrency.objects.get(symbol=request.POST['crypto']),
                crypto_amount=float(request.POST['quantity']),
                amount_paid=float(request.POST['total_price']),
                amount_currency=FiatCurrency.objects.get(symbol=request.POST['fiat']),
                date_time=datetime.now(),
                transactions_type=False,
                status=True
            )

            new_transaction.save()

            msgToRtrn = "Payment processed successfully."
        else:
            msgToRtrn = "You have less amount " + cryptoCurrency.symbol + " amount in your Wallet, Try again."

        return render(request, 'checkout.html', {'msg': msgToRtrn})


class checkoutSuccess(View):
    def get(self, request):
        msgToRtrn = ""
        try:
            paymentId = request.GET['payment_intent']
            intent = stripe.PaymentIntent.retrieve(paymentId)
            clientSecret = intent['client_secret']
            if intent.status == 'succeeded':
                transaction = Transaction.objects.get(secret_key=clientSecret, user=request.user.id)
                if transaction.id > 0:
                    transaction.status = True
                    transaction.save()
                    msgToRtrn = 'Payment processed successfully.'
                else:
                    msgToRtrn = 'Payment not successful. fake request.'
            else:
                msgToRtrn = 'Payment not successful.'
        except stripe.error.StripeError as e:
            msgToRtrn = "Unable to process payment, server side error, try again later"

        return render(request, 'checkout.html', {'msg': msgToRtrn})


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


class HomeView(TemplateView):
    template_name = 'home.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'privacy_policy.html'


class TermsOfServiceView(TemplateView):
    template_name = 'terms_of_service.html'


# user transaction history view
def crypto_table_view(request):
    transactions = Transaction.objects.filter(user=request.user.id)
    return render(request, 'transaction.html', {'data': transactions})


# user wallet view
def user_wallet_view(request):
    all_transactions = Transaction.objects.filter(user=request.user.id)

    # Use a defaultdict to store the sum for each crypto_currency_id
    sum_by_currency = defaultdict(float)

    # Calculate the sum for each crypto_currency_id
    for transaction in all_transactions:
        if transaction.transactions_type:
            sum_by_currency[transaction.crypto_currency_id] += transaction.crypto_amount
        else:
            sum_by_currency[transaction.crypto_currency_id] -= transaction.crypto_amount

    # Fetch CryptoCurrency objects for the related currency IDs
    currency_objects = CryptoCurrency.objects.in_bulk(sum_by_currency.keys())

    # Create a list with the currency name, ID, and total sum
    sums = [
        {
            'currency_name': currency_objects[currency_id].name,
            'currency_id': currency_id,
            'total_sum': total_sum,
        }
        for currency_id, total_sum in sum_by_currency.items()
    ]

    all_f_transactions = ForexTransaction.objects.filter(user=request.user.id)

    # Use a defaultdict to store the sum for each crypto_currency_id
    sum_by_f_currency = defaultdict(float)

    # Calculate the sum for each crypto_currency_id
    for transaction in all_f_transactions:
        sum_by_f_currency[transaction.forex_currency_id] += transaction.currency_amount_purchased

    # Fetch CryptoCurrency objects for the related currency IDs
    currency_f_objects = FiatCurrency.objects.in_bulk(sum_by_currency.keys())

    # Create a list with the currency name, ID, and total sum
    f_sums = [
        {
            'currency_name': currency_f_objects[currency_id].name,
            'currency_id': currency_id,
            'total_sum': total_sum,
        }
        for currency_id, total_sum in sum_by_f_currency.items()
    ]

    # # You can access the sums by crypto_currency_id in the sum_by_currency dictionary
    # for currency_id, total_sum in sum_by_currency.items():
    #     print(f"Total sum for crypto_currency_id {currency_id}: {total_sum}")
    return render(request, 'wallet.html', {'data': sums, 'f_data':f_sums})


# sell view

class ForexView(LoginRequiredMixin, View):
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
        return render(request, "selling.html", context=context)
