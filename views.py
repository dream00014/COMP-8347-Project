from django.shortcuts import render, get_object_or_404

from .models import Coin


# Create your views here.
# views.py
import requests
from django.shortcuts import render


def coin_list(request):
    # CoinGecko API endpoint for listing all supported coins
    api_url = 'https://api.coingecko.com/api/v3/coins/list'

    # Specify the parameters, include_platform set to true
    params = {'include_platform': 'true'}

    # Make a GET request to the CoinGecko API
    response = requests.get(api_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        coins = response.json()

        # Render the template with the retrieved data
        return render(request, 'coin_list.html', {'coins': coins})
    else:
        # If the request was not successful, handle the error
        return render(request, 'error.html', {'error_message': 'Failed to fetch coin data from CoinGecko API'})


def coin_detail(request, coin_id):
    api_url = f'https://api.coingecko.com/api/v3/coins/{coin_id}'
    params = {'localization': 'false', 'sparkline': 'true'}

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        coin_data = response.json()
        return render(request, 'coin_detail.html', {'coin_data': coin_data})
    except requests.exceptions.RequestException as e:
        return render(request, 'error.html', {'error_message': f'Error fetching coin detail: {e}'})