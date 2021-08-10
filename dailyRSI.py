import pandas_datareader as pdr
import datetime as dt
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd

should_continue = True
while should_continue == True:
    data = []
    ticker_file = open('tickers.txt', 'r+')
    ticker_input = ticker_file.read()
    #User inputs
    # ticker_input = input("Enter Stock Tickers (separated by whitespaces): ")
    ticker_list = ticker_input.split(' ')
    for x in ticker_list:
        ticker = pdr.get_data_yahoo(x, dt.datetime(int(2020),int(1),int(1)), dt.datetime.now())


        difference = ticker['Close'].diff()
        up = difference.clip(lower=0)
        down = -1*difference.clip(upper=0)
        e_up = up.ewm(com=13, adjust=False).mean()
        e_down = down.ewm(com=13, adjust=False).mean()
        relative_strength = e_up/e_down

        ticker['RSI'] = 100 - (100/(1 + relative_strength))

        #Skip first 14 days to void dummy values
        #ticker = ticker.iloc[14:]
        data.append([x, ticker.iloc[-1][6]])
        df = pd.DataFrame(data, columns = ['Ticker', 'RSI Value'])
    print('RSI as of ' + str(date.today()))
    print(df)
    df.to_csv(str(date.today()) + 'rsi.csv', index = False)
    
    # again = input('Would you like to run this program again? (y/n): ')
    # if again == 'n':
    should_continue = False
