from django.contrib import admin
from .models import CryptoCurrency, FiatCurrency, CurrencyExchangeInfo, Transaction, ForexTransaction

# Register your models here.

@admin.register(CryptoCurrency)
class CryptoCurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol']


@admin.register(FiatCurrency)
class FiatCurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol']

@admin.register(CurrencyExchangeInfo)
class CurrencyExchangeInfoAdmin(admin.ModelAdmin):
    list_display = ['crypto_currency']
    list_filter = ['fiat_currency', 'crypto_currency']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['crypto_currency']

@admin.register(ForexTransaction)
class ForexTransactionAdmin(admin.ModelAdmin):
    list_display = ['forex_currency']