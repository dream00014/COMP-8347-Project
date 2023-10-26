from django.db import models

# Create your models here.


class DigitalCurrency(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField()
    website = models.CharField(max_length=100)
    # past_price = models.


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    head_photo = models.ImageField()
    email_address = models.EmailField()


class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='PaymentMethod')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    Currency = models.ForeignKey(DigitalCurrency)