from django.urls import path
from .views import coin_list, coin_detail

app_name = 'COMP8345'

urlpatterns = [
    path('coinlist', coin_list, name='coinlist'),
    path('COMP8345/coin/<str:coin_id>/', coin_detail, name='coin_detail'),
]