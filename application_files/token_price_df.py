import pandas as pd
from datetime import datetime
import requests
import json



def check_token_history(token):
       
        token_url = f"https://api.coingecko.com/api/v3/coins/{token}/market_chart"
        params = {
            'id': token,
            'vs_currency': 'USD',
            'days': 'max', 
            'interval': 'daily'
        }
        token_response = requests.get(url=token_url, params=params)
        support_token_json = json.loads(token_response.content)


        return support_token_json
            

def timestamp_todate(timestamp):
        # devide timestamp by 1000 to remove milliseconds for conversion 
        date_return = datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d')
        return date_return


def coin_gecko_supports(token):
    """
    returns token_id for coingecko if supported, false otherwise
    """


    url_request = requests.get('https://api.coingecko.com/api/v3/coins/list')
    if url_request.status_code != 200:
        raise ConnectionError
    json_response = json.loads(url_request.content)
    
    df = pd.json_normalize(json_response)

    symbol = list(df['symbol'])
    name = list(df['name'])
    token_id = list(df['id'])

    if token in symbol:
        index = symbol.index(token)
        token = token_id[index]
        return token 

    return False

def main(token):
    """
    given a coingecko token id, returns a pandas DF that has two columns [date, price]
    """
    token_hist = check_token_history(token)

    df = pd.DataFrame(token_hist['prices'], columns=['date', 'price'])

    df['date'] = df['date'].map(lambda d: timestamp_todate(d))

    return (df[::-1])
