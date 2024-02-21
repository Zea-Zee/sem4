import requests
from requests import Request, Session
from requests.exceptions import Timeout, ConnectionError, TooManyRedirects
from colorama import Back, Style, init as colorama_init
import os
import sys
import json
import time


import pandas as pd


PAIRS_LIMIT = 500


colorama_init()


DATA_PATH = (str(os.path.dirname(os.path.abspath(__file__))) + '/data/')


def build_min_max_cost_pairs(token_slug):
    try:
        with open(DATA_PATH + 'market_pairs/' + token_slug + '_markets' + '.json') as f:
            data = json.load(f)

        df = pd.DataFrame(data)
        # df = df[df['marketPair'].str.startswith("BTC/USD")]
        # df[] = df.groupby('marketPair').agg(max_price=('price', 'max'), min_price=('price', 'min'))
        # result = result[result]
        df.to_csv(token_slug + '.csv')

    except Exception as e:
        print(f"{Back.RED}build_min_max_cost_pairs:\n{e}{Back.RESET}")



def get_all_tokens_id():
    ids = []
    try:
        with open(DATA_PATH + 'map.json', 'r', encoding='utf-8') as f:
            tokens = json.load(f)

        for obj in tokens['data']:
            ids.append(obj['id'])
        return ids
    except Exception as e:
        print(f"{Back.RED}get_all_tokens_id:\n{e}{Back.RESET}")


def print_temp_text(text, sleep_time, back_color_code=None, is_last=False):
    if not back_color_code:
        back_color_code = Back.RESET
    sys.stdout.write("\033[K")
    sys.stdout.write("\r")
    sys.stdout.write(back_color_code + text + Back.RESET)
    sys.stdout.flush()
    if sleep_time is not None:
        time.sleep(sleep_time)
    if is_last:
        print('')


def get_cryptocurrency_identifiers(key_name, key_val):
    try:
        with open(os.path.join(DATA_PATH, 'map.json'), 'r') as map_file:
            tokens = json.load(map_file)

        for obj in tokens['data']:
            if obj[key_name] == key_val:
                return (obj['slug'], obj['id'], obj['name'], obj['symbol'], obj['rank'])

        raise ValueError(
            f"Can't find object in data with key_name {key_name} and key_val {key_val}")
    except Exception as e:
        print(
            Back.RED, f"Exception in get_cryptocurrency_slug func: {e}", Style.RESET_ALL)
        raise ValueError(e)


def open_token_page(key_name, key_val, session):
    try:
        slug = get_cryptocurrency_identifiers(key_name, key_val)[0]
        print(f"{Back.MAGENTA}{slug} market pairs{Back.RESET}")
        url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/market-pairs/latest"
        params = {
            "slug": slug,
            "category": "spot",
            "centerType": "all",
            "sort": "cmc_rank_advanced",
            "direction": "desc",
            "spotUntracked": "true"
        }

        market_pairs = []

        # for start_num in range(1, 6002, 1000):

        start_num = 1
        while(True):
            params['start'] = start_num
            params['limit'] = PAIRS_LIMIT

            print_temp_text(url + f"?start={start_num}&limit={PAIRS_LIMIT}", None, Back.YELLOW)
            response = session.get(url, params=params)
            if response.ok:
                print_temp_text(url + f"?start={start_num}&limit={PAIRS_LIMIT}", None, Back.GREEN, True)
            else:
                break

            if response.json()['status']['error_code'] != '0':
                break
            if not ('marketPairs' in response.json()['data']):
                # json.dump(response.json(), sys.stdout)
                break
            market_pairs.extend(response.json()['data']['marketPairs'])

            start_num += PAIRS_LIMIT
        with open(DATA_PATH + '/market_pairs/' + slug + '_markets.json', 'w', encoding='utf-8') as f:
                json.dump(market_pairs, f)

    except Exception as e:
        print(
            Back.RED, f"Exception in open_token_page func: {e}", Style.RESET_ALL)
    print('')



# session = Session()
# ids = get_all_tokens_id()
# print(len(ids))

build_min_max_cost_pairs('bitcoin')
# for id in ids:
#     if id < 2397:
#         continue
#     open_token_page('id', id, session)

# open_token_page('id', 1, session)
# open_token_page('symbol', 'BTC', session)
# open_token_page('symbol', 'ETH', session)
# open_token_page('symbol', 'ETC', session)
# open_token_page('symbol', 'USDT', session)
