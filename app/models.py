from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class CryptoCurrency(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    symbol = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(default="")
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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    id_document = models.ImageField(upload_to='id_documents/', blank=True, null=True)

    def __str__(self):
        return self.user.username

from django.db import models
from django.contrib.auth.models import User

#Crypto transaction model
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    secret_key = models.TextField()
    crypto_currency = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE)
    crypto_amount = models.FloatField()
    amount_paid = models.FloatField()
    amount_currency = models.ForeignKey(FiatCurrency, on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=datetime.now())
    transactions_type = models.BooleanField(default=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s {self.crypto_currency.name} Transaction"


#Forex transaction model
class ForexTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto_currency = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE)
    crypto_amount_paid = models.FloatField()
    currency_amount_purchased = models.FloatField()
    forex_currency = models.ForeignKey(FiatCurrency, on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=datetime.now())
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s {self.crypto_currency.name} Transaction"