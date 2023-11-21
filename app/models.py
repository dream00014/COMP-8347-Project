from django.db import models

# Create your models here.


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

#sp
# class CryptoDetails(models.Model):
#     crypto = models.ForeignKey(
#         CryptoCurrency, on_delete=models.CASCADE, null=False, blank=False
#     )
#     description = models.TextField()
#     exchange_rate = models.DecimalField(max_digits=15, decimal_places=8)
#
#     def __str__(self):
#         return self.crypto

