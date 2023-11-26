from django.urls import path
from . import views
from .views import HomeView
from .views import PrivacyPolicyView
from .views import TermsOfServiceView



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

    path("home/", HomeView.as_view(), name='home'),
    path("login/", views.LoginView.as_view(), name="login_view"),

    path("signup/", views.SignUpView.as_view(), name="signup_view"),
    path("logout/", views.LogoutView.as_view(), name="logout_view"),
    path('crypto/', views.CryptoSelectionView.as_view(), name='crypto_selection'),
    path('payment/', views.PaymentView.as_view(), name='crypto_payment'),
    path('sell/', views.SellView.as_view(), name='forex_payment'),

    path('checkout/', views.checkoutSuccess.as_view(), name='crypto_payment_checkout'),

    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-of-service/', TermsOfServiceView.as_view(), name='terms_of_service'),
    path('transactions/', views.crypto_table_view, name='user_transactions'),
    path('user-wallet/', views.user_wallet_view, name='user_wallet'),
    path(
        "selling/<str:selected_crypto>/",
        views.ForexView.as_view(),
        name="forex_exchange",
    ),


]
