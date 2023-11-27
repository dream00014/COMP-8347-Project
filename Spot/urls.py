from Spot import views
from django.urls import path

app_name = 'currency'

urlpatterns = [
    path('detail/<int:spot_id>/', views.spot_currency, name='spot_detail'),
    path('', views.index, name='spot_index')
]