# Anna W. For learning/skill retention

import IPython.core.display

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf

from datetime import datetime
from plotly.subplots import make_subplots

def get_yf_data(ticker_list, start_date, end_date):
    """
    Connects to the yfinance API and pulls stock information data based
    on input parameter conditions.
    
    :param [String] ticker_list: String list containing stock ticker 
        codes for companies.
    :param datetime start_date: Start date to get stock performance 
        range.
    :param datetime end_date: End date to get stock performance range.
    :return pd.DataFrame: Dataframe containing valuation data for the 
        supplied stock codes within the supplied date range.
    """

    df_list = []

    # Loop through ticker list and call yfinance API to pull stock data 
    for ticker in ticker_list:
        ticker_df = yf.download(ticker, start=start_date, end=end_date)
        df_list.append(ticker_df)

    # Concat all stock information in one dataframe
    stock_perf_df = pd.concat(df_list, keys=ticker_list, names=['Ticker', 'Date'])
    stock_perf_df = stock_perf_df.reset_index()

    print(stock_perf_df.head())

    return stock_perf_df


def show_stock_performance_graphs(stock_perf_df):
    """
    Show basic performance graphs of the stock data.
    - line_fig shows a line graph that plots the open and close price 
        of each stock over the requested time period.
    - area_fig better shows the movement and performance of each stock.
    
    :param pd.DataFrame stock_perf_df: Dataframe containing stock data 
        over a defined time frame.
    """

    line_fig = px.line(stock_perf_df,
                x='Date',
                y='Close',
                color='Ticker',
                title='Stock Market Performance for the Last 3 Months ($USD)')
    
    line_fig.show()
    
    area_fig = px.area(stock_perf_df,
                       x='Date',
                       y='Close',
                       color='Ticker',
                       facet_col='Ticker',
                       labels={'Date': 'Date', 'Close': 'Closing Price', 'Ticker': 'Company'},
                       title='Stock prices for Apple, Google, Nvidia, and Netflix ($USD)')
    
    area_fig.show()
    
    
def calc_moving_averages(stock_perf_df):
    """
    Show the moving averages of stock close prices. A simple moving 
    average (SMA) is an indicator to help determine the direction 
    of a stock trend. SMAs smooth out the volatility of the 
    day-over-day movement of the stock.
    
    :param pd.DataFrame stock_perf_df: Dataframe containing stock 
        data over a defined time frame.
    """
    # Create a copy of the original df
    moving_avg_df = stock_perf_df.copy()
    
    # Calculate moving averages using pandas rolling() and mean()
    moving_avg_df['Moving Avg. 10 Days'] = moving_avg_df.groupby('Ticker')['Close'].rolling(window=10).mean().reset_index(0, drop=True)
    moving_avg_df['Moving Avg. 20 Days'] = moving_avg_df.groupby('Ticker')['Close'].rolling(window=20).mean().reset_index(0, drop=True)
        
    # Show moving averages in graph format
    subplot_list = []
    subplot_titles_list = []
    
    # We will create a subplot for each ticker and then combine them using make_subplots to easily view on one window
    for ticker, group in moving_avg_df.groupby('Ticker'):
        print(f'Moving averages for: {ticker}')
        print(group[['Moving Avg. 10 Days', 'Moving Avg. 20 Days']])
        
        fig = px.line(group,
                      x='Date',
                      y=['Close', 'Moving Avg. 10 Days', 'Moving Avg. 20 Days'],
                      title=f'{ticker} Moving Averages ($USD)')
        subplot_list.append(fig)
        subplot_titles_list.append(ticker)
        
    fig = make_subplots(rows=4, 
                        cols=1, 
                        shared_xaxes=False, 
                        subplot_titles=subplot_titles_list) 
    
    # "Concatenate" each of the three subplots (Close, Moving Avg. 10 Days, Moving Avg. 20 Days) per ticker
    for i in range(len(subplot_list)):
        fig.add_trace(subplot_list[i]['data'][0], row=i+1, col=1)
        fig.add_trace(subplot_list[i]['data'][1], row=i+1, col=1)
        fig.add_trace(subplot_list[i]['data'][2], row=i+1, col=1)
        
    # Bug with multiple legends - need to convert the graph building to a graph_object
    # but running into issues using the grouping. Will continue to work on fixing.
    # Hiding legend for now
    fig.update_layout(showlegend=False)
    fig.show()
    
    
def calc_stock_volatility(stock_perf_df):
    """
    Show the volatility of stock close prices. Higer volatility 
    indicates that the stock experiences large and frequent price 
    movements.
    
    :param pd.DataFrame stock_perf_df: Dataframe containing stock data 
        over a defined time frame.
    """
    # Create a copy of the original df
    volatility_df = stock_perf_df.copy()

    # Do the same approach as above with the moving average, but calculate the standard deviation of the close price
    # We are using pandas default settings - Normalized by N-1
    volatility_df['Volatility'] = volatility_df.groupby('Ticker')['Close'].pct_change().rolling(window=10).std().reset_index(0, drop=True)

    # Show a outputs in graph format
    fig = px.line(volatility_df,
                  x='Date',
                  y='Volatility',
                  color='Ticker',
                  title='Volatility of all Stocks')
    
    fig.show()

def show_stock_correlation(stock_perf_df):
    """
    Shows the correlation between two stocks. Stocks can show similar 
    growth trends if they are in similar industries, have similar 
    market conditions, or common business parters or customers.

    :param pd.DataFrame stock_perf_df: Dataframe containing stock data 
        over a defined time frame.
    """
    
    # Create a DataFrame with the stock prices of Apple and Microsoft
    apple_df = stock_perf_df.loc[stock_perf_df['Ticker'] == 'NVDA', ['Date', 'Close']].rename(columns={'Close': 'NVDA'})
    microsoft_df = stock_perf_df.loc[stock_perf_df['Ticker'] == 'MSFT', ['Date', 'Close']].rename(columns={'Close': 'MSFT'})
    
    stock_corr_df = pd.merge(apple_df, microsoft_df, on='Date')

    # Create a scatter plot to visualize the correlation
    fig = px.scatter(stock_corr_df, 
                     x='NVDA', 
                     y='MSFT', 
                     trendline='ols', 
                     title='Correlation between Nvidia and Microsoft')
    
    fig.show()
            

def main():
    """
    Driver function for code. you can modify 
    """
    print("Running stock prediction model...")

    # Parameters below >>>
    
    start_date = datetime.now() - pd.DateOffset(months=3)
    end_date = datetime.now()

    ticker_list = ['AAPL', 'GOOG', 'NVDA', 'MSFT']
    
    # >>> End parameters
    
    stock_perf_df = get_yf_data(ticker_list, start_date, end_date)

    show_stock_performance_graphs(stock_perf_df)
        
    calc_moving_averages(stock_perf_df)
    
    calc_stock_volatility(stock_perf_df)
    
    show_stock_correlation(stock_perf_df)
    
main()