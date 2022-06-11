import requests
import json
import pandas as pd
import os


class WalletResponseError (ConnectionError):
    """Raised when connecting to the input wallet address does not connect properly (all purpose response status code handling)"""
    pass

class EmptyWalletError(KeyError):
    """"Raised if input wallet has no reward value
    can be returned for invalid wallet OR wallet with no LP rewards"""
    pass

def total_reward(dict):
    a = 0
    total = 0
    for i in dict:
        if (a == len(dict) - 1):
         return total
        a = a + 1

        total = total + float(dict[a]['amount'])
    return total



def token_data(name, wallet):
    """
    returns historical list of rewards given a wallet address and token name
    """
 
    print(f'checking {name} rewards history')
    
    url = f'https://api-osmosis-chain.imperator.co/lp/v1/rewards/historical/{wallet}/{name}'
    rewards_response = requests.get(url = url)
    
    #get total/price of rewards
    rewards_list = json.loads(rewards_response.content)
      
    total = total_reward(rewards_list)
      

    return [name, rewards_list, total]



def main(wallet):
    """
given a wallet address, gets history of token rewards, appending a csv file in
    the cwd with each tokens reward history. returns all tokens as json object
    """

    url_token_list = f'https://api-osmosis-chain.imperator.co/lp/v1/rewards/token/{wallet}'
    token_list_response = requests.get(url=url_token_list)

    if token_list_response.status_code != 200:
        raise WalletResponseError()

    # url content returns an empty list if the address isnt valid OR no rewards for wallet (empty list == False) 
    elif not json.loads(token_list_response.content): 
        raise EmptyWalletError()


    tokens = json.loads(token_list_response.content)

    daily_token = []
    date_list = [] 
    for i in tokens:
        name = i['token'].lower()

        # get daily reward list
        reward_data = token_data(name=name, wallet=wallet)
        daily_list = (reward_data[1][:]) 
        
        # convert data to dataframe to save as .csv
        for i in daily_list:
            daily_token.append(i['amount'])
            date_list.append(i['day'])

        token_info = {'date': date_list, 'amount': daily_token}
        token_df = pd.DataFrame(token_info)

        cwd = os.getcwd()
        reward_file_path = f'{cwd}\\osmo_profit_tracker\\data_files\\reward_hist\\{name}_rewards.csv'
            
        print('saved ', reward_file_path[67:], '\n')
        token_df.to_csv(reward_file_path.lower())
        

        # reset lists for next iteration
        daily_token = []
        date_list = []

    return tokens
 
