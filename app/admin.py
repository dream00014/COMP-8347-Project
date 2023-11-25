from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(CryptoCurrency)
class CryptoCurrencyAdmin(admin.ModelAdmin):
    list_display = ["name", "symbol"]


@admin.register(FiatCurrency)
class FiatCurrencyAdmin(admin.ModelAdmin):
    list_display = ["name", "symbol"]


@admin.register(CurrencyExchangeInfo)
class CurrencyExchangeInfoAdmin(admin.ModelAdmin):
    list_display = ["crypto_currency"]
    list_filter = ["fiat_currency", "crypto_currency"]


@admin.register(TransactionHistory)
class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ["transaction_id", "user", "transaction_type", "transaction_status"]
    list_filter = ["transaction_id", "user", "transaction_type", "transaction_status"]
