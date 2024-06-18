import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf

from datetime import datetime
from plotly.subplots import make_subplots

def get_yf_data(ticker_list, start_date, end_date):

    df_list = []

    for ticker in ticker_list:
        ticker_df = yf.download(ticker, start=start_date, end=end_date)
        df_list.append(ticker_df)

    stock_perf_df = pd.concat(df_list, keys=ticker_list, names=['Ticker', 'Date'])
    stock_perf_df = stock_perf_df.reset_index()

    print(stock_perf_df.head())

    return stock_perf_df


def show_stock_performance_graphs(stock_perf_df):

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
    

def show_stock_performance_graphs2(df):

    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=df['Date'],
                       y=df['Close'],   
                       mode='lines',
                       legend=df['Ticker'])
                  
                    )
    fig.update_layout(
        title='Stock Market Performance for the Last 3 Months ($USD)',
        legend_title='Tickers'
    )
    fig.show()
    
    # fig = make_subplots(rows=2, 
    #                 cols=1, 
    #                 shared_xaxes=False, 
    #                 subplot_titles=['Stock Market Performance for the Last 3 Months ($USD)',
    #                                 'Stock prices for Apple, Google, Nvidia, and Netflix ($USD)']) 
    
    # fig.add_trace(line_fig['data'][0], row=1, col=1)
    # fig.add_trace(area_fig['data'][0], row=2, col=1)
    
    # fig.show()
    
    
def calc_moving_averages(stock_perf_df):
    moving_avg_df = stock_perf_df.copy()
    
    moving_avg_df['Moving Avg. 10 Days'] = moving_avg_df.groupby('Ticker')['Close'].rolling(window=10).mean().reset_index(0, drop=True)
    moving_avg_df['Moving Avg. 20 Days'] = moving_avg_df.groupby('Ticker')['Close'].rolling(window=20).mean().reset_index(0, drop=True)
    
    for ticker, group in moving_avg_df.groupby('Ticker'):
        print(f'Moving averages for: {ticker}')
        print(group[['Moving Avg. 10 Days', 'Moving Avg. 20 Days']])
        
    # Show moving averages in graph format
    subplot_list = []
    subplot_titles_list = []
    
    for ticker, group in moving_avg_df.groupby('Ticker'):
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
    volatility_df = stock_perf_df.copy()

    volatility_df['Volatility'] = volatility_df.groupby('Ticker')['Close'].pct_change().rolling(window=10).std().reset_index(0, drop=True)

    fig = px.line(volatility_df,
                  x='Date',
                  y='Volatility',
                  color='Ticker',
                  title='Volatility of all Stocks')
    
    fig.show()

def show_stock_correlation(stock_perf_df):
    
    # create a DataFrame with the stock prices of Apple and Microsoft
    apple_df = stock_perf_df.loc[stock_perf_df['Ticker'] == 'AAPL', ['Date', 'Close']].rename(columns={'Close': 'AAPL'})
    microsoft_df = stock_perf_df.loc[stock_perf_df['Ticker'] == 'GOOG', ['Date', 'Close']].rename(columns={'Close': 'GOOG'})
    
    stock_corr_df = pd.merge(apple_df, microsoft_df, on='Date')

    # create a scatter plot to visualize the correlation
    fig = px.scatter(stock_corr_df, 
                     x='AAPL', 
                     y='GOOG', 
                     trendline='ols', 
                     title='Correlation between Apple and Google')
    
    fig.show()
            

def main():
    print("Running stock prediction model...")

    start_date = datetime.now() - pd.DateOffset(months=3)
    end_date = datetime.now()

    ticker_list = ['AAPL', 'GOOG', 'NVDA', 'NFLX']

    stock_perf_df = get_yf_data(ticker_list, start_date, end_date)

    show_stock_performance_graphs(stock_perf_df)
        
    calc_moving_averages(stock_perf_df)
    
    calc_stock_volatility(stock_perf_df)
    
    show_stock_correlation(stock_perf_df)
    
main()