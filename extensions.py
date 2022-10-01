import requests
import json
from conf import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if base == quote:
            raise APIException('Нечего конвертировать :)')

        try:
            ticker_q = keys[quote]
        except KeyError:
            raise APIException(f'Неправильная валюта {quote}')

        try:
            ticker_b = keys[base]
        except KeyError:
            raise APIException(f'Некорректная валюта {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Некорректная сумма: {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={ticker_q}&tsyms={ticker_b}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base * amount
