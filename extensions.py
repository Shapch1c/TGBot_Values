import requests
import json
from config import CURRENCIES

class APIException(Exception):
    pass

class CurrencyConverter:
    API_KEY = '7f82f9a91c3d0008d5f6d7b7cbd802ed'
    BASE_URL = 'http://api.currencylayer.com/'

    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        base = base.lower()
        quote = quote.lower()

        if base == quote:
            raise APIException("Невозможно перевести одинаковые валюты.")

        try:
            base_ticker = CURRENCIES[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {base}")

        try:
            quote_ticker = CURRENCIES[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {quote}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}")

        url = f"{CurrencyConverter.BASE_URL}convert"
        params = {
            'from': base_ticker,
            'to': quote_ticker,
            'amount': amount,
            'access_key': CurrencyConverter.API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        if not data.get('success', False):
            raise APIException("Ошибка при получении курса валют.")

        return round(data['result'], 4)
