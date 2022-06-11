import sys

# custom modules
import reward_to_csv
import combine_price_rewards


def main(wallet):   

    # returns list of different tokens rewarded for that wallet
    # creates csv file in data_files directory that lists amount received each day, for each token rewarded
    try:        
        token_list = reward_to_csv.main(wallet=wallet)
      
    except reward_to_csv.WalletResponseError:
        print(f'Could not connect to wallet {wallet}')
        input('Any key to exit:')
        sys.exit()

    except reward_to_csv.EmptyWalletError:
        print('Wallet has no osmo LP reward data')
        input('Any key to exit:')
        sys.exit()

    print('rewards history saved in data_files\\reward_hist\\')
    print('\ncombining price data\n')

    for token in token_list:
        t = token['token'].lower()

        # true for t successful profit csv generation from rewards data and price history data(coingecko)
        if (combine_price_rewards.main(t)):
            print(f'success: {t} profit .csv saved')
        else:
            print(f'failed: {t} ')



if __name__ == '__main__':

    wallet = ''  ###### <-- input osmosis wallet address here
    main(wallet)