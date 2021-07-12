import requests
import os


def get_crypto_info():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    headers = {
        'X-CMC_PRO_API_KEY': os.environ.get('api_key'),
        'Accepts': 'application/json'
    }

    params = {
        'start': '1',
        'limit': '100',
        'convert': 'USD'
    }

    json_data = requests.get(url, params=params, headers=headers).json()
    cryptos = json_data['data']

    required_fields = ['name', 'symbol', 'price', 'percent_change_24h', 'market_cap']
    new_dict = {}
    list_dict = []

    for x, i in enumerate(cryptos):
        for (outer_k, outer_v) in i.items():
            if outer_k in required_fields:
                new_dict.update({outer_k: outer_v})
            if outer_k == "quote":
                for (inner_k, inner_v) in outer_v.items():
                    if inner_k == "USD":
                        for (ik, iv) in inner_v.items():
                            if ik in required_fields:
                                new_dict.update({ik: iv})
        new_dict.update({'id': x+1})
        list_dict.append(new_dict.copy())


    return list_dict