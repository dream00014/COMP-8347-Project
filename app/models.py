from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class CryptoCurrency(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    symbol = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class FiatCurrency(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    symbol = models.CharField(max_length=100, null=True, blank=True)
    # price = models.PositiveBigIntegerField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class CurrencyExchangeInfo(models.Model):
    crypto_currency = models.ForeignKey(
        CryptoCurrency, on_delete=models.CASCADE, null=False, blank=False
    )
    fiat_currency = models.ForeignKey(
        FiatCurrency, on_delete=models.CASCADE, blank=False
    )
    price = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.crypto_currency.name


class TransactionHistory(models.Model):

    TRANSACTION_TYPES = (
        ("BUY", "BUY"),
        ("SELL", "SELL"),
    )

    TRANSACTION_STATUS = (
        ("SUCCESSED", "SUCCESSED"),
        ("FAILED", "FAILED"),
        ("PENDING", "PENDING"),
    )

    TRANSACTION_CURRENCY = (
        ("CRYPTO", "CRYPTO"),
        ("FIAT", "FIAT"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True)
    transaction_type = models.CharField(max_length=100, choices=TRANSACTION_TYPES, null=False, blank=False)
    transaction_status = models.CharField(max_length=100, choices=TRANSACTION_STATUS, null=False, blank=False)
    from_currency = models.CharField(max_length=100, choices=TRANSACTION_CURRENCY, null=True, blank=True)
    from_currency_qty = models.IntegerField(null=False, blank=False)
    to_currency = models.CharField(max_length=100, choices=TRANSACTION_CURRENCY, null=True, blank=True)
    to_currency_amount = models.DecimalField(max_digits=10, decimal_places=3, null=False, blank=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=3, null=False, blank=False)
    
    def __str__(self):
        return self.user.username
    