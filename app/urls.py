from django.urls import path
from . import views

urlpatterns = [
    path("", views.PortfolioView.as_view(), name="portfolio_view"),
    path(
        "exchange/<str:selected_crypto>/",
        views.ExchangeView.as_view(),
        name="exchange_view",
    ),
    path(
        "get-price/<str:crypto_symbol>/<str:fiat_symbol>/",
        views.GetExchangePrice.as_view(),
        name="get_exchange_price_view",
    ),
    path("login", views.LoginView.as_view(), name="login_view"),
    path("signup", views.SignUpView.as_view(), name="signup_view"),
    path("logout", views.LogoutView.as_view(), name="logout_view"),
]
