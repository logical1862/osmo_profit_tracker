import pandas as pd
import os

# custom module
import token_price_df as token_df


# class to hold values for combined df
class profit_table():
    def __init__(self) -> None:
        self.profit = [] # type: list
        self.date = []  # type: list
        self.reward = [] # type: list
        self.price = [] # type: list

    def append_table(self, profit: list, date: list, reward: list, price: list):
        """
    appends data in profit_table instance with lists passed in ,

    tab = profit_table()
    tab.append_table(profit=profit, date=date, reward=reward, price=price)
        """
        self.profit.append(profit)
        self.date.append(date)
        self.reward.append(reward)
        self.price.append(price)


def main(token):
    """
    reads rewards data of < token > output by reward_to_csv.main()

    if < token > is supported by coin gecko api creates a price history data frame to generate a, 

        total_profit.csv. joined on similar date format in rewards data and price data,

        returns True if successful

            False if not supported  
    """
    
    profit_tab = profit_table()

    cwd = os.getcwd()
    reward_data_path = R"{}\osmo_profit_tracker\data_files\reward_hist\{}_rewards.csv".format(cwd, token)
    
    try:
        token_id = token_df.coin_gecko_supports(token)
    except ConnectionError:
        return False
    if (token_id):
    
        price_df = token_df.main(token_id)    

        reward_df = pd.read_csv(reward_data_path, encoding='utf8', index_col=0)

        for row in reward_df.values:
            reward_date = row[0]
            reward_amount = row[1]
            for row2 in price_df.values:
                price_date = row2[0]
                price_value = row2[1]

                # if dates in both data frames match, append profit table with (date, amount rewarded, price of token that day(via coingecko),
                #  and calculated profit for that day)
                if reward_date == price_date:
                    profit_tab.append_table(profit=(price_value*reward_amount) , date=reward_date, reward=reward_amount, price=price_value)

        data = {
            'date': profit_tab.date,
            'reward': profit_tab.reward,
            'price': profit_tab.price,
            'profit': profit_tab.profit
        }
        combined = pd.DataFrame(data)

        # to add record date ( using last date of reward as record date) to file name, check for empty list before indexing latest date entry
        file_path_less_date = f"{cwd}\\osmo_profit_tracker\\data_files\\profits\\{token}_total_profit_"
        if not profit_tab.date:
            date = 'NONE'
        else:
            date = profit_tab.date[0]

        combined.to_csv(f'{file_path_less_date}{date}.csv')
        return True

    else:
        return False