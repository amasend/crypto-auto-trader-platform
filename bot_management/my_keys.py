from binance.client import Client

def api_test_key():
    return '1pQAddCJB4k1ql6Yh2PE9fqmbq1uXOCDTB7fAfPYAd1R9bCesOJiYiCTaYEbEwAW'


def api_test_secret_key():
    return 'p8cytjkESoUm9WlmCnvdRSGkA45WEKZr6Ub3yg2uD3vFRUEcp6meNCtcTMl0UDet'


def api_real_key():
    return 'FcveizhPmdMWRsQlVJrxvRUIjgom0h35VMGeqtnzbUrr8TPS9RI8UiT3QqFGJcWs'


def api_real_secret_key():
    return 'KGFxZR1piNYqFdrwURijVFlw7EXXA7aZHaVqv8Qx8fz6WDX6LPgqetlpbk36wdsv'

def binance_client():
    return Client(api_test_key(),api_test_secret_key())