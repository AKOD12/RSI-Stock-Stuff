import yfinance as yf, pandas as pd
import numpy as np
import pandas_datareader as pdr
import datetime as dt
import requests
from get_all_tickers import get_tickers as gt
from statistics import mean, stdev
import matplotlib.pyplot as plt
import statistics
import time
import scipy.stats as stats
import math

should_continue = True
while should_continue == True:
    #User inputs
    ticker_input = input("Enter Stock Ticker: ")
    start_year = input("Enter Start Year: ")
    start_month = input("Enter Start Month: ")
    start_day = input("Enter Start Day: ")
    ticker = pdr.get_data_yahoo(ticker_input, dt.datetime(int(start_year),int(start_month),int(start_day)), dt.datetime.now())


    difference = ticker['Close'].diff()
    up = difference.clip(lower=0)
    down = -1*difference.clip(upper=0)
    e_up = up.ewm(com=13, adjust=False).mean()
    e_down = down.ewm(com=13, adjust=False).mean()
    relative_strength = e_up/e_down

    ticker['RSI'] = 100 - (100/(1 + relative_strength))

    #Skip first 14 days to void dummy values
    #ticker = ticker.iloc[14:]

    current_rsi_ask = input("Would you like the most recent RSI for " + ticker_input + "? (y/n): ")
    if current_rsi_ask == 'y':
        print("The most recent RSI for " + ticker_input + " is " + str(ticker.iloc[-1][6]))



    ticker.to_csv(ticker_input + '.csv', index = False)
    #Adjust stock name as needed
    df = pd.read_csv(ticker_input + '.csv')


    #Adjust these as desired
    min_rsi = input("Enter an RSI Lower Bound: ")
    #max_rsi = input("Enter an RSI Upper Bound: ")
    period = input("Enter a Period of Days to be Observed: ")

    min_rsi = int(min_rsi)
    #max_rsi = int(max_rsi)
    period = int(period)

    #Takes data from only the last recent days

    low_rsi_price_changes = []
    low_rsi_percent_changes = []

    high_rsi_price_changes = []
    high_rsi_percent_changes = []

    below_instance = 0
    #For when observing after RSI hits certain low point
    for index,row in df.iterrows():
        if row[6] < min_rsi and row[6] != 0:
            below_instance += 1
        try:
            start_price = row[5]
            end_price = df.iloc[index + period][5]
            low_rsi_price_changes.append(end_price-start_price)
            low_rsi_percent_changes.append(((end_price-start_price)/start_price)*100)
        except:
            IndexError

    print("The RSI went below " + str(min_rsi) + ' ' + str(below_instance) + " times")

    if below_instance > 0:
        low_avg = statistics.mean(low_rsi_percent_changes)
        low_var = np.var(low_rsi_percent_changes)
        low_stdev = math.sqrt(low_var)
        x = np.linspace(low_avg - 4*low_stdev, low_avg + 4*low_stdev, 100)
        plt.plot(x, stats.norm.pdf(x, low_avg, low_stdev))
        plt.axvline(x = low_avg, linestyle = 'dashed', color = 'green')
        plt.axvline(x = low_avg + low_stdev, linestyle = 'dashed', color = 'green')
        plt.axvline(x = low_avg + 2*low_stdev, linestyle = 'dashed', color = 'green')
        plt.axvline(x = low_avg + 3*low_stdev, linestyle = 'dashed', color = 'green')
        plt.axvline(x = low_avg + 4*low_stdev, linestyle = 'dashed', color = 'green')
        plt.axvline(x = low_avg - low_stdev, linestyle = 'dashed', color = 'green')
        plt.axvline(x = low_avg - 2*low_stdev, linestyle = 'dashed', color = 'green')
        plt.axvline(x = low_avg - 3*low_stdev, linestyle = 'dashed', color = 'green')
        plt.axvline(x = low_avg - 4*low_stdev, linestyle = 'dashed', color = 'green')
        plt.title('Normal Distribution of percent changes for ' + ticker_input + ' when RSI < ' + str(min_rsi) +  ' days after ' + str(period) + ' days')
        plt.xlabel('Percent Change')
        plt.ylabel('Probability')
        see_low_graph = input("Would you like to see the bell curve for the RSI lower bound? (y/n): ")
        if see_low_graph == 'y':
            plt.show()
        low_rsi_price_change_average = round(statistics.mean(low_rsi_price_changes),4)
        low_rsi_percent_changes_average = round(statistics.mean(low_rsi_percent_changes),4)
        print('The average price change when the RSI was < ' + str(min_rsi) + ' was ' + '$' + str(low_rsi_price_change_average))
        print('The average percent change when the RSI was < ' + str(min_rsi) + ' was ' + str(low_rsi_percent_changes_average) + '%')

    prompt_continue = input('Would you like to run this program again? (y/n): ')
    print('\n')
    if prompt_continue == 'n':
        should_continue = False


    # above_instance = 0
    # #For when observing after RSI hits certain high point
    # for index,row in df.iterrows():
    #     if row[6] > max_rsi and row[6] != 0:
    #         above_instance += 1
    #         try:
    #             start_price = row[5]
    #             end_price = df.iloc[index + period][5]
    #             high_rsi_price_changes.append(end_price-start_price)
    #             high_rsi_percent_changes.append(((end_price-start_price)/start_price)*100)
    #         except:
    #             IndexError

    # if above_instance > 0:
    #     high_avg = statistics.mean(high_rsi_percent_changes)
    #     high_var = np.var(high_rsi_percent_changes)
    #     high_stdev = math.sqrt(high_var)
    #     y = np.linspace(high_avg - 4*high_stdev, high_avg + 4*high_stdev, 100)
    #     plt.plot(y, stats.norm.pdf(y, high_avg, high_stdev))
    #     plt.axvline(x = high_avg, linestyle = 'dashed', color = 'green')
    #     plt.axvline(x = high_avg + high_stdev, linestyle = 'dashed', color = 'green')
    #     plt.axvline(x = high_avg + 2*high_stdev, linestyle = 'dashed', color = 'green')
    #     plt.axvline(x = high_avg + 3*high_stdev, linestyle = 'dashed', color = 'green')
    #     plt.axvline(x = high_avg + 4*high_stdev, linestyle = 'dashed', color = 'green')
    #     plt.axvline(x = high_avg - high_stdev, linestyle = 'dashed', color = 'green')
    #     plt.axvline(x = high_avg - 2*high_stdev, linestyle = 'dashed', color = 'green')
    #     plt.axvline(x = high_avg - 3*high_stdev, linestyle = 'dashed', color = 'green')
    #     plt.axvline(x = high_avg - 4*high_stdev, linestyle = 'dashed', color = 'green')
    #     plt.title('Normal Distribution of percent changes for ' + ticker_input + ' when RSI > ' + str(max_rsi) + ' after ' + str(period) + ' days')
    #     plt.xlabel('Percent Change')
    #     plt.ylabel('Probability')
    #     plt.show()

    # high_rsi_price_change_average = round(statistics.mean(high_rsi_price_changes),4)
    # high_rsi_percent_changes_average = str(round(statistics.mean(high_rsi_percent_changes),4)) + " %"

