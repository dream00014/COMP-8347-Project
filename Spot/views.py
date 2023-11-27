from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404

from Spot.forms import SpotSearchForm, ScoreForm
from Spot.models import DigitalCurrency, MarketingRate, Spot, Score, Customer


# Create your views here.


def home(request):
    return render(request, 'info/home.html')


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
            return redirect('currency:spot_detail', spot_id=spot_id)
    else:
        form = ScoreForm()

    return render(request, 'info/spotDetail.html', {'form': form,
                                                    'spot': spot,
                                                    'user_score': user_score,
                                                    'userInfo': userInfo,
                                                    })



