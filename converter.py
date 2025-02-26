import requests

def get_exchange_rates(base_currency="USD"):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["rates"]
    else:
        raise Exception("Failed to fetch exchange rates")

def convert_currency(amount, from_currency, to_currency):
    rates = get_exchange_rates(from_currency)
    if to_currency in rates:
        return amount * rates[to_currency]
    else:
        raise Exception("Target currency not available")
