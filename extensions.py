import requests
import json
from config import keys

class ConvertException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote:str, base:str, amount:str):
        if quote == base:
            raise ConvertException('Нельзя конвертировать валюту в такую же.')

        try:
            currency_1 = keys[quote]
        except KeyError:
            raise ConvertException(f'Не удалось обнаружить валюту {quote}')

        try:
            currency_2 = keys[base]
        except KeyError:
            raise ConvertException(f'Не удалось обнаружить валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException(f'Не удалось обработать количество "{amount}"')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={currency_1}&tsyms={currency_2}')
        total = json.loads(r.content)[keys[base]]

        return total