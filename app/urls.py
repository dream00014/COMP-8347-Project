
from . import views
from django.urls import path, register_converter

register_converter(views.FloatUrlParameterConverter, 'float')


urlpatterns = [
    path("", views.CryptoView.as_view(), name="crypto_view"),
    path("<str:filter_by>", views.CryptoView.as_view(), name="filter_view"),
    path("exchange/<str:symbol>/<str:fiat_currency>/<float:fiat_value>", views.ExchangeView.as_view(), name="exchange_view")
]
