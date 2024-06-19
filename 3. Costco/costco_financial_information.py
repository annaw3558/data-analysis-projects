import pandas as pd
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
    stock_perf_df = pd.concat(df_list, keys=ticker_list, names=["Ticker", "Date"])
    stock_perf_df = stock_perf_df.reset_index()

    print(stock_perf_df.head())

    return stock_perf_df


def calc_price_change(stock_perf_df):
    """
    Calculates some simple performance metrics for stocks.
    1. Percent change
    2. 20 Day Moving Average
    3. 100 Day Moving Average

    :param pd.DataFrame stock_perf_df: Dataframe containing stock 
        data over a defined time frame.
    :return Pandas Dataframe: Modified stock performance df with new
        columns added.
    """
    stock_perf_df["Adj Previous Close"] = stock_perf_df["Adj Close"].shift(1)
    stock_perf_df["Adj Pct Change"] = stock_perf_df[["Open","Adj Previous Close"]].pct_change(axis=1)["Adj Previous Close"]
    
    stock_perf_df["Previous Close"] = stock_perf_df["Close"].shift(1)
    stock_perf_df["Pct Change"] = stock_perf_df[["Open","Previous Close"]].pct_change(axis=1)["Previous Close"]
    
    stock_perf_df['20 Day MA'] = stock_perf_df.groupby('Ticker')['Adj Close'].rolling(window=20).mean().reset_index(0, drop=True)
    stock_perf_df['100 Day MA'] = stock_perf_df.groupby('Ticker')['Adj Close'].rolling(window=100).mean().reset_index(0, drop=True)  
    
    stock_perf_df = stock_perf_df.drop(axis=1, columns=["Adj Previous Close", "Previous Close", "High", "Low"])
    
    return stock_perf_df
    
def main():
    """
    Driver function for code. you can modify 
    """
    print("Running stock prediction model...")

    # Parameters below >>>
    
    start_date = datetime.now() - pd.DateOffset(months=12)
    end_date = datetime.now()

    # Costco, Walmart, Kroger
    ticker_list = ["COST", "WMT", "KR"]
    
    # >>> End parameters
    stock_perf_df = get_yf_data(ticker_list, start_date, end_date)
        
    stock_perf_df = calc_price_change(stock_perf_df)
    
    print(stock_perf_df)
    
main()