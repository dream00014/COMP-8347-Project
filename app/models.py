from django.db import models
from django.contrib.auth.models import User

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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    id_document = models.ImageField(upload_to='id_documents/', blank=True, null=True)

    def __str__(self):
        return self.user.username


# Create your models here.

# Yang Wang's database models

class Customer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    head_photo = models.ImageField()
    email_address = models.EmailField()
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name+" "+self.last_name

    def get_full_name(self):
        return self.first_name+" "+self.last_name


class DigitalCurrency(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField()
    website = models.CharField(max_length=100)
    describe = models.CharField(max_length=2000)
    interest = models.ManyToManyField(Customer, blank=True, related_name='digital_currency')

    def __str__(self):
        return self.name


class RealCurrency(models.Model):
    name = models.CharField(max_length=5)
    price = models.FloatField()

    def __str__(self):
        return self.name


class PairType(models.Model):
    pair_1 = models.ForeignKey(DigitalCurrency, on_delete=models.CASCADE, related_name='pair')
    pair_2 = models.ForeignKey(RealCurrency, on_delete=models.CASCADE, related_name='pair')

    def __str__(self):
        return self.pair_1.name+' '+self.pair_2.name


class PaymentMethod(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='PaymentMethod')
    method = models.CharField(max_length=10, default='')

    def __str__(self):
        return self.user.first_name+' '+self.user.last_name


class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='order')
    Currency = models.ForeignKey(DigitalCurrency, on_delete=models.CASCADE, related_name='order')


class Spot(models.Model):
    name = models.CharField(max_length=20)
    web_link = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    score = models.IntegerField(default=5)
    volume = models.IntegerField(default=100000000)
    liquidity = models.IntegerField(default=100000000)
    weekly_visit = models.IntegerField(default=100000000)
    markets = models.IntegerField(default=100000000)
    coins = models.IntegerField(default=100000000)
    flat = models.ManyToManyField('RealCurrency', blank=True, related_name='spot')

    def __str__(self):
        return self.name

    def calculate_score(self):
        scores = self.score_info.all()

        if scores.exists():
            total = sum(score.score for score in scores)
            ave = total / scores.count()
            self.score = round(ave, 1)
            self.save()
        else:
            self.score = 5
            self.save()


class Score(models.Model):
    score_choice = [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='score_info')
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name='score_info')
    score = models.IntegerField(choices=score_choice, default=5)

    def __str__(self):
        return self.user.get_full_name()+" "+self.spot.name+" "+str(self.score)

    class Meta:
        unique_together = (
            'user',
            'spot',
        )


class CurrencyDetail(models.Model):
    time = models.DateTimeField()
    exchange_rate = models.PositiveIntegerField()
    currency = models.ForeignKey(DigitalCurrency, on_delete=models.CASCADE, related_name='detail')


class MarketingRate(models.Model):
    time = models.DateTimeField()
    pair = models.ForeignKey(PairType, on_delete=models.CASCADE, related_name='market_rate')
    exchange_rate = models.PositiveIntegerField()
    market = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name='market')


class Reserve(models.Model):
    currency_type = models.ForeignKey('DigitalCurrency', on_delete=models.CASCADE, related_name='reserve_currency')
    spot = models.ForeignKey('Spot', on_delete=models.CASCADE, related_name='reserve_spot')
    balance = models.FloatField()
    price = models.FloatField()
    value = models.FloatField()

    def __str__(self):
        return self.spot.name

