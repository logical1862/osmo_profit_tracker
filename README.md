# osmo_profit_tracker
 *compatible only with Osmo wallet address see https://osmosis.zone/ , part of the larger Cosmos 'Internet of Blockchains' see https://cosmos.network/
 *for reference only, not to be used with with any official financial reporting


  Track daily LP rewarded tokens and their cost-basis amount via calls to the osmo API and CoinGecko API. 

  Calls wallet LP rewards data, which saves a csv file of each token rewarded to  \osmo_profit_tracker\data_files\reward_hist

  Calls combine_price_rewards.py to combine historical price data:

    -check token name against supported coins
    -calls token_price_df to:
            -return pandas dataframe with price history
    -concat reward history with price history. Joined on matching dates. 
    -cost basis calculated.
    -saves to .csv file in  \osmo_profit_tracker\data_files\profits\

  configure wallet address through the wallet variable in osmo_profit_main.py
  check requirements.txt in application_data for library versions 