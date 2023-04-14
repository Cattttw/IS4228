# -*- coding: utf-8 -*-
"""IS4228 Data Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AyMZ9aGMbjutWRdGiuC9O5qXj2aGqlBS

#Investor 1
The investor is young, has a low income, low savings and high risk appetite. Wealthfront recommended a risk level of 9. 

This includes a 45% of US stocks (VTI), 18% of Foreign stocks (VEA), 17% of emerging market stocks(VWO), 11% of dividen growth stock (VIG) and 9% of municipal bonds (VTEB).
"""

!pip install yfinance  
import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf 
import statistics as st
import math
import matplotlib.pyplot as plt
from pandas_datareader.data import DataReader
from scipy.stats import norm
from sklearn import linear_model

winget install pandoc

def get_data_for_multiple_stocks(tickers, start_date, end_date):
    '''
    Function that uses Pandas DataReader to download data directly from Yahoo Finance,
    computes the Log Returns series for each ticker, and returns a DataFrame 
    containing the Log Returns of all specified tickers.
    
    Parameters:
    - tickers (list): List of Stock Tickers.
    - start_date, end_date (str): Start and end dates in the format 'YYYY-MM-DD'.
    
    Returns:
    - returns_df (pd.DataFrame): A DataFrame with dates as indexes, and columns corresponding to the log returns series of each ticker.
    '''
    # initialise output dataframe
    returns_df = pd.DataFrame()
    price_df = pd.DataFrame()
    
    for ticker in tickers:
        # retrieve stock data (includes Date, OHLC, Volume, Adjusted Close)
        format='%Y-%m-%d'
        s = yf.download(ticker, dt.datetime.strptime(start_date, format), dt.datetime.strptime(end_date, format))
        price_df[ticker] = s['Adj Close']
        # calculate log returns
        s['Percentage Returns'] = s['Adj Close']/s['Adj Close'].shift(1) - 1
        # append to returns_df
        returns_df[ticker] = s['Percentage Returns']     
    # skip the first row (that will be NA)
    # and fill other NA values by 0 in case there are trading halts on specific days
    returns_df = returns_df.iloc[1:].fillna(0)       
    return returns_df, price_df

tickers = ["VTI", "VEA", "VWO", "VIG", "VTEB"]
returns_df, price_df = get_data_for_multiple_stocks(tickers, start_date = '2020-01-01', end_date = '2022-12-31')
returns_df.head()

dateIndex = returns_df.index

plt.plot(dateIndex, returns_df.VTI,label = "VTI")
plt.plot(dateIndex, returns_df.VEA,label = "VEA")
plt.plot(dateIndex, returns_df.VWO,label = "VWO")
plt.plot(dateIndex, returns_df.VIG,label = "VIG")
plt.plot(dateIndex, returns_df.VTEB,label = "VTEB")

plt.xlabel("Date")
plt.ylabel("3-year percentage return of 5 assets")

plt.legend()


plt.savefig('/content/drive/MyDrive/image 1.png', dpi=300)

import seaborn as sb

dataplot = sb.heatmap(returns_df.corr(), cmap="YlGnBu", annot=True)
  
# displaying heatmap


plt.savefig('/content/drive/MyDrive/heat map.png', dpi=300)

weight = [.45, .18, .17, .11, .09]
portfolio_intial_price = 10000

portfolio_initial_value = list(map(lambda x: x * portfolio_intial_price, weight))
portfolio_intial_shares = portfolio_initial_value / price_df.iloc[0].values
portfolio_intial_shares

from dateutil.relativedelta import relativedelta

format = "%Y-%m-%d"

start = dt.datetime.strptime("2020-01-01", format)
end = dt.datetime.strptime("2022-12-31", format)

quarter = []

this_q = start
for i in range(50):
  quarter.append(this_q)
  this_q += relativedelta(months = 3)

quarter
i = 1
curr_quarter = quarter[i]
curr_quarter

price_df.head()

this_date = start

portfolio_prices = []
portfolio_shares = portfolio_intial_shares


#weights = [[200, 1000, 1000],]


while this_date <= end:
  if this_date in price_df.index:
    #readjusting the portfolio
    if this_date > curr_quarter:

      i+= 1
      curr_quarter = quarter[i]

      last_day_price = portfolio_prices[-1]
      
      portfolio_value = list(map(lambda x: x * last_day_price, weight))
      portfolio_shares = portfolio_value / price_df.loc[str(this_date.date())].values

    portfolio_prices.append((portfolio_shares * price_df.loc[str(this_date.date())]).sum())


  this_date += dt.timedelta(days = 1)

price_df_portfolio = price_df.copy()
price_df_portfolio["Portfolio"] = portfolio_prices

returns_df_portfolio = returns_df.copy()
returns_df_portfolio["Portfolio"] = price_df_portfolio["Portfolio"]/price_df_portfolio["Portfolio"].shift(1) - 1

dateIndex = returns_df.index

plt.plot(dateIndex, returns_df_portfolio.VTI,label = "VTI", linewidth = 0.6)
plt.plot(dateIndex, returns_df_portfolio.VEA,label = "VEA", linewidth = 0.6)
plt.plot(dateIndex, returns_df_portfolio.VWO,label = "VWO", linewidth = 0.6)
plt.plot(dateIndex, returns_df_portfolio.VIG,label = "VIG", linewidth = 0.6)
plt.plot(dateIndex, returns_df_portfolio.VTEB,label = "VTEB", linewidth = 0.6)
plt.plot(dateIndex, returns_df_portfolio.Portfolio,label = "Portfolio", linewidth = 0.6)

plt.xlabel("Date")
plt.ylabel("3-year return of 5 assets & Portfolio")

plt.legend()

plt.savefig('/content/drive/MyDrive/Return Asset + Portfolio.png', dpi=300)

returns_df.head()

returns_df.loc[str(this_date.date()-dt.timedelta(days = 2))].VTI

this_date = start

cumulative_return_VTI = [1,]
cumulative_return_VEA = [1,]
cumulative_return_VWO = [1,]
cumulative_return_VIG = [1,]
cumulative_return_VTEB = [1,]
cumulative_return_Portfolio = [1,]

while this_date <= end:
  if this_date in returns_df.index:
   
    cumulative_return_VTI.append(cumulative_return_VTI[-1]*(1 + returns_df_portfolio.loc[str(this_date.date())].VTI))
    cumulative_return_VEA.append(cumulative_return_VEA[-1]*(1 + returns_df_portfolio.loc[str(this_date.date())].VEA))
    cumulative_return_VWO.append(cumulative_return_VWO[-1]*(1 + returns_df_portfolio.loc[str(this_date.date())].VWO))
    cumulative_return_VIG.append(cumulative_return_VIG[-1]*(1 + returns_df_portfolio.loc[str(this_date.date())].VIG))
    cumulative_return_VTEB.append(cumulative_return_VTEB[-1]*(1 + returns_df_portfolio.loc[str(this_date.date())].VTEB))
    cumulative_return_Portfolio.append(cumulative_return_Portfolio[-1]*(1 + returns_df_portfolio.loc[str(this_date.date())].Portfolio))


  this_date += dt.timedelta(days = 1)

cumulative_returns_df = returns_df.copy()
cumulative_returns_df.VTI = cumulative_return_VTI[1:]
cumulative_returns_df.VEA = cumulative_return_VEA[1:]
cumulative_returns_df.VWO = cumulative_return_VWO[1:]
cumulative_returns_df.VIG = cumulative_return_VIG[1:]
cumulative_returns_df.VTEB = cumulative_return_VTEB[1:]
cumulative_returns_df.Portfolio = cumulative_return_Portfolio[1:]

dateIndex = returns_df.index

plt.plot(dateIndex, cumulative_returns_df.VTI,label = "VTI", linewidth = 0.8)
plt.plot(dateIndex, cumulative_returns_df.VEA,label = "VEA", linewidth = 0.8)
plt.plot(dateIndex, cumulative_returns_df.VWO,label = "VWO", linewidth = 0.8)
plt.plot(dateIndex, cumulative_returns_df.VIG,label = "VIG", linewidth = 0.8)
plt.plot(dateIndex, cumulative_returns_df.VTEB,label = "VTEB", linewidth = 0.8)
plt.plot(dateIndex, cumulative_returns_df.Portfolio,label = "Portfolio", linewidth = 0.8)

plt.xlabel("Date")
plt.ylabel("3-year cumulative return of 5 assets and portfolio")

plt.legend()


plt.savefig('/content/drive/MyDrive/cumulative return.png', dpi=300)

log_return = np.log(returns_df_portfolio + 1)
log_return

meanLogReturn_VTI = st.mean(log_return.VTI)
meanLogReturn_VEA = st.mean(log_return.VEA)
meanLogReturn_VWO = st.mean(log_return.VWO)
meanLogReturn_VIG = st.mean(log_return.VIG)
meanLogReturn_VTEB = st.mean(log_return.VTEB)
meanLogReturn_Portfolio = st.mean(log_return.Portfolio)

SDLogReturn_VTI = np.std(log_return.VTI)
SDLogReturn_VEA = np.std(log_return.VEA)
SDLogReturn_VWO = np.std(log_return.VWO)
SDLogReturn_VIG = np.std(log_return.VIG)
SDLogReturn_VTEB = np.std(log_return.VTEB)
SDLogReturn_VTEB = np.std(log_return.Portfolio)

dateIndex = returns_df.index

plt.plot(SDLogReturn_VTI, meanLogReturn_VTI,"o", label = "VTI")
plt.plot(SDLogReturn_VEA, meanLogReturn_VEA,"o", label = "VEA")
plt.plot(SDLogReturn_VWO, meanLogReturn_VWO,"o", label = "VWO")
plt.plot(SDLogReturn_VIG, meanLogReturn_VIG,"o", label = "VIG")
plt.plot(SDLogReturn_VTEB, meanLogReturn_VTEB,"o", label = "VTEB")
plt.plot(SDLogReturn_VTEB, meanLogReturn_Portfolio,"o", label = "Portfolio")

plt.xlabel("Risk / Volatility")
plt.ylabel("Expected return over the 2-year period")

plt.legend()
plt.savefig('/content/drive/MyDrive/risk volatility.png', dpi=300)

