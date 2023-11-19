# project/urls.py
from django.contrib import admin
from django.urls import path, include
from myTradingapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usersettingpage/', views.user_settings, name='usersettingpage'),
    path('', include('myTradingapp.urls'))
    # Add other app URLs or patterns as needed
]
