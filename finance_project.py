from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime

import matplotlib.pyplot as plt
import seaborn as sns
import plotly
import cufflinks as cf
cf.go_offline()

# Define Start and Endpoint for data time frame
start = datetime.datetime(2006,1,1)
end = datetime.datetime(2016,1,1)

# Download Data
BAC = data.DataReader('BAC','yahoo',start,end) #BankofAmerica
C = data.DataReader('C','yahoo',start,end) #CitiGroup
GS = data.DataReader('GS','yahoo',start,end) #Goldman Sachs
JPM = data.DataReader('JPM','yahoo',start,end) #JPMorgan Chase
MS = data.DataReader('MS','yahoo',start,end) #Morgan Stanley
WFC = data.DataReader('WFC','yahoo',start,end) #Wells Fargo

# Create usefull column titles
tickers = ['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC']
bank_stocks = pd.concat([BAC,C,GS,JPM,MS,WFC], axis=1,keys=tickers)
bank_stocks.columns.names = ['Bank Ticker','Stock Info']

# Create Dataframe for the return values
returns = pd.DataFrame()
for tick in tickers:
    returns[tick+' Return'] = bank_stocks[tick]['Close'].pct_change()

# Figure 1: Example of return values for 2015 of Morgan Stanley and Citigroup
plt.figure()
sns.distplot(returns.loc['2008-01-01':'2008-12-31']['MS Return'], color='red', bins=50)
plt.show()

plt.figure()
sns.distplot(returns.loc['2008-01-01':'2008-12-31']['C Return'], color='green', bins=50)
plt.show()


# Figure 2: Close price for each Bank over the entire daterange
plt.figure()
for tick in tickers:
    bank_stocks[tick]['Close'].plot(label=tick,figsize=(12,6))
plt.legend()
plt.title('Close price between 2006 and 2016')
plt.show()
#bank_stocks.xs(key='Close',axis=1,level='Stock Info').plot(figsize=(12,4))

# Figure 3: Moving Averages for Bank of America in 2008
plt.figure(figsize=(12,6))
BAC['Close'].loc['2008-01-01':'2009-01-01'].rolling(window=30).mean().plot(label='30 Day moving average')
BAC['Close'].loc['2008-01-01':'2009-01-01'].plot(label='BAC Close')
plt.legend()
plt.title('Moving Average for BAC in 2008')
plt.show()

# Figure 4: Clustermap of correlation bewtwen stocks close prices
corrClosePrice = bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr()

sns.clustermap(corrClosePrice, cmap='coolwarm', annot=True)
plt.title('Clustermap of Correlation betweeen stock close prices')
plt.show()

plt.figure()
bac15 = BAC[['Open','High', 'Low','Close']].loc['2015-01-01':'2016-01-01']
bac15.iplot(kind='candle')
plt.show()