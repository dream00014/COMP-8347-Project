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


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    ]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name", "email")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
