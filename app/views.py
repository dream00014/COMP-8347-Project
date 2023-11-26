from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import *
from django.views import View
from django.forms.models import model_to_dict
import requests
from .forms import RankingFilterForm, LoginForm, SignUpForm, ScoreForm, SpotSearchForm
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
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class PortfolioView(LoginRequiredMixin, View):
    login_url = "/login"

    def get(self, request):
        userInfo = request.user
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

        context = {"form": form, "data": data, 'userInfo': userInfo}

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


class PaymentView(View):
    def post(self, request):
        intent = stripe.PaymentIntent.create(
            amount= int(float(request.POST['total_price'])),
            currency='usd',
            automatic_payment_methods={
                'enabled': True,
            },
        )

        # store data into temp transactions table
        print(intent['client_secret'])

        return render(request, 'payment.html', {'form': intent['client_secret'], 'crypto_type' : request.POST['crypto'], 'crypto_qty' : request.POST['quantity']})


class CheckoutSuccess(View):
    def get(self, request):
        return render(request, 'checkout.html')


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # 在这里 user 和相应的 Customer 已经被创建
            return redirect("login_view")
        else:
            return render(request, "signup.html", {"form": form})


class HomeView(TemplateView):
    template_name = 'home.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'privacy_policy.html'


class TermsOfServiceView(TemplateView):
    template_name = 'terms_of_service.html'


# Yang Wang's views


def index(request):
    userInfo = request.user
    form = SpotSearchForm(request.GET or None)
    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')

        min_score = form.cleaned_data.get('min_score')
        max_score = form.cleaned_data.get('max_score')

        # min_volume = form.cleaned_data.get('min_volume')
        # max_volume = form.cleaned_data.get('max_volume')

        # min_liquidity = form.cleaned_data.get('min_liquidity')
        # max_liquidity = form.cleaned_data.get('max_liquidity')

        # min_weekly = form.cleaned_data.get('min_weekly')
        # max_weekly = form.cleaned_data.get('max_weekly')

        # min_markets = form.cleaned_data.get('min_markets')
        # max_markets = form.cleaned_data.get('max_markets')

        # min_coins = form.cleaned_data.get('min_coins')
        # max_coins = form.cleaned_data.get('max_coins')

        query = Spot.objects.all()
        if keyword:
            query = query.filter(name__icontains=keyword)

        if min_score is not None:
            query = query.filter(score__gte=min_score)
        if max_score is not None:
            query = query.filter(score__lte=max_score)

        # if min_volume is not None:
        #     query = query.filter(score__gte=min_volume)
        # if max_volume is not None:
        #     query = query.filter(score__lte=max_volume)
        #
        # if min_liquidity is not None:
        #     query = query.filter(score__gte=min_liquidity)
        # if max_liquidity is not None:
        #     query = query.filter(score__lte=max_liquidity)
        #
        # if min_weekly is not None:
        #     query = query.filter(score__gte=min_weekly)
        # if max_weekly is not None:
        #     query = query.filter(score__lte=max_weekly)
        #
        # if min_markets is not None:
        #     query = query.filter(score__gte=min_markets)
        # if max_markets is not None:
        #     query = query.filter(score__lte=max_markets)
        #
        # if min_coins is not None:
        #     query = query.filter(score__gte=min_coins)
        # if max_coins is not None:
        #     query = query.filter(score__lte=max_coins)

        spot_list = query
    else:
        spot_list = Spot.objects.all()

    for spot in spot_list:
        spot.calculate_score()

    context = {
        "spot_list": spot_list,
        "form": form,
        "userInfo": userInfo,
    }
    return render(request, 'info/spotList.html', context)


def detail_currency(request, currency_id):
    digitalCurrency = DigitalCurrency.objects.get(id=currency_id)
    market_all = MarketingRate.objects.all()
    market_list = {}
    for market in market_all:
        if market.pair.pair_1.id == currency_id:
            market_list.update(market)

    context = {
        'market_list': market_list,
        'digitalCurrency': digitalCurrency,
    }
    return render(request, 'info/currencyDetail.html', context)


def spot_currency(request, spot_id):
    userInfo = request.user
    spot = get_object_or_404(Spot, pk=spot_id)
    customer_user = Customer.objects.get(user=request.user)
    user_score = None

    # 检查当前用户是否已经评分
    try:
        score_obj = Score.objects.get(user=customer_user, spot=spot)
        user_score = score_obj.score
    except Score.DoesNotExist:
        user_score = None

    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            score_value = form.cleaned_data['score']
            Score.objects.update_or_create(
                user=customer_user,
                spot=spot,
                defaults={'score': score_value}
            )
            spot.calculate_score()
            return redirect('spot_detail', spot_id=spot_id)
    else:
        form = ScoreForm()

    return render(request, 'info/spotDetail.html', {'form': form,
                                                    'spot': spot,
                                                    'user_score': user_score,
                                                    'userInfo': userInfo,
                                                    })


def user_logout(request):
    request.session.flush()
    return render(request, 'home.html')


# Jiyu's view:


def coin_list(request):
    userInfo = request.user
    # CoinGecko API endpoint for listing all supported coins
    api_url = 'https://api.coingecko.com/api/v3/coins/list'

    # Specify the parameters, include_platform set to true
    params = {'include_platform': 'true'}

    # Make a GET request to the CoinGecko API
    response = requests.get(api_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        coins = response.json()

        # Render the template with the retrieved data
        return render(request, 'info/coin_list.html', {'coins': coins,
                                                       'userInfo': userInfo,
                                                       })
    else:
        # If the request was not successful, handle the error
        return render(request, 'info/error.html', {'error_message': 'Failed to fetch coin data from CoinGecko API',
                                                   'userInfo': userInfo,
                                                   })


def coin_detail(request, coin_id):
    userInfo = request.user
    api_url = f'https://api.coingecko.com/api/v3/coins/{coin_id}'
    params = {'localization': 'false', 'sparkline': 'true'}

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        coin_data = response.json()
        return render(request, 'info/coin_detail.html', {'coin_data': coin_data,
                                                         'userInfo': userInfo,
                                                         })
    except requests.exceptions.RequestException as e:
        return render(request, 'info/error.html', {'error_message': f'Error fetching coin detail: {e}',
                                                   'userInfo': userInfo,
                                                   })
