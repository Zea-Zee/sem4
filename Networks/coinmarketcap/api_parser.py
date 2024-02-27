from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from colorama import Fore, Back, Style, init
import sys
import os


init()

api_key = ""
try:
    api_key_path = (
        str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/trash.json"
    )
    file = open(api_key_path, "r")
    api_key = json.load(file)["apiKeys"]["coinmarketcap.com"]
    file.close()
except Exception as e:
    print(Fore.RED + "Can't read api_key: " + str(e), Style.RESET_ALL)
    sys.exit(1)


base_url = "https://pro-api.coinmarketcap.com/"
urls_dict = {
    "categories": base_url + "v1/cryptocurrency/categories",
    "map": base_url + "v1/cryptocurrency/map",
    "exchange": base_url + "v1/exchange/map",
    "test": "https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest",
    "test_BTC": "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC",
    "info": "https://pro-api.coinmarketcap.com/v1/key/info",
}

headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": api_key,
}

session = Session()
session.headers.update(headers)

try:
    save_path = (
        str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        + "/networks/data"
    )
    for key, value in urls_dict.items():
        print(Back.YELLOW, f"Requesting {value}", Style.RESET_ALL)
        response = session.get(value)
        response.raise_for_status()
        data = response.json()
        output = open(f"{save_path}//{key}.json", "w")
        output.write(json.dumps(data))
        output.close()
        print(
            Back.GREEN, f"{value} has sucessfully loaded and written", Style.RESET_ALL
        )
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
