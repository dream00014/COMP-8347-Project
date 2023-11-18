from django.shortcuts import render, HttpResponse
from django.views import View
import requests
import json
from .forms import RankingFilterForm

# Create your views here.


# class CryptoView(View):
#     def get(self, request, page_number=None, filter_by=None):
#         # from Tradingbeez.settings import ALPHA_VOLTAGE_API_KEY
#         # key = ALPHA_VOLTAGE_API_KEY
#         # # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
#         # url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey={key}'
#         # r = requests.get(url)
#         # data = r.json()

#         # # print(json.dumps(data))

#         # data = json.dumps(data)
#         # context = {}
#         # context['data'] = data
#         # # print(context)


#         form = RankingFilterForm()
#         api_url = "https://api.coincap.io/v2"
#         endpoint = "assets"
#         params = {}
#         page_number = 1


#         if filter_by is not None:
#             limit_per_page = 10
#             if filter_by == "top":
#                 params = {
#                     "limit": limit_per_page,
#                     "offset": (page_number - 1) * limit_per_page,
#                 }
#             elif filter_by == "worst":
#                 params = {
#                     "limit": limit_per_page,
#                     "offset": (11 - 1) * limit_per_page,
#                 }


#         response = requests.get(f"{api_url}/{endpoint}", params=params)
#         data = response.json()

#         print(data)

#         context = {}
#         context["data"] = data
#         context["page_number"] = page_number
#         context["form"]= form
#         return render(request, "crypto.html", context=context)


class CryptoView(View):
    def get(self, request, filter_by=None):
        form = RankingFilterForm(request.GET)

        api_url = "https://api.coincap.io/v2"
        endpoint = "assets"
        params = {}
        page_number = 1

        # print(form,"===========>>>>>>>>>")

        if filter_by is not None:
            limit_per_page = 10
            if filter_by == "top":
                params = {
                    "limit": limit_per_page,
                    "offset": (page_number - 1) * limit_per_page,
                }
            elif filter_by == "worst":
                params = {
                    "limit": limit_per_page,
                    "offset": (100 - limit_per_page),
                }

        response = requests.get(f"{api_url}/{endpoint}", params=params)
        data = response.json()

        print("\n\n", data, "\n\n")
        context = {
            "data": data,
            "page_number": page_number,
            "form": form,
        }
        return render(request, "crypto.html", context=context)


class PaginnationView(View):
    def get(self, request):
        data = request.get("data")


class ExchangeView(View):
    def get(self, request, symbol, fiat_currency, fiat_value):
        print(symbol, "========SYMBOL")
        print(fiat_currency, "========SYMBOL")
        print(fiat_value, "========SYMBOL")

        context = {
            "symbol": symbol,
            "fiat_currency": fiat_currency,
            "fiat_value": fiat_value
        }
        return render(request, "exchange.html", context=context)


class FloatUrlParameterConverter:
    regex = "[0-9]+\.?[0-9]+"

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)
