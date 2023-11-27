from django.contrib import admin

from Spot.models import DigitalCurrency, RealCurrency, PairType, Customer, \
    PaymentMethod, Order, Spot, CurrencyDetail, MarketingRate, Score, Reserve

# admin edit


class DigitalCurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


class RealCurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


class SpotAdmin(admin.ModelAdmin):
    list_display = ['name', 'web_link']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email_address']


class ScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'spot', 'score']


class ReservesAdmin(admin.ModelAdmin):
    list_display = ['spot', 'currency_type', 'balance', 'price', 'value']


# Register your models here.

admin.site.register(DigitalCurrency, DigitalCurrencyAdmin)
admin.site.register(RealCurrency, RealCurrencyAdmin)
admin.site.register(PairType)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(PaymentMethod)
admin.site.register(Order)
admin.site.register(Spot, SpotAdmin)
admin.site.register(CurrencyDetail)
admin.site.register(MarketingRate)
admin.site.register(Score, ScoreAdmin)
admin.site.register(Reserve, ReservesAdmin)
