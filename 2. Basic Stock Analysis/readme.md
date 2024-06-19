## Basic Stock Analysis

Inspired by an article by Aman Kharwal ([linked here](https://thecleverprogrammer.com/2023/05/08/stock-market-performance-analysis-using-python/))

### Main Goal
I wanted to provide a public example of my knowledge in pandas and dealing with stock data, and also explore some visualization methods used to help identify stock trends and performance.

### Packages Used
- yfinance
- pandas
- plotly

### Findings
Below are screenshots of the outputed graphs in the program. We look at the recorded close prices of four publicly traded companies: Apple (APPL), Google (GOOG), Microsoft (MSFT), and Nvidia (NVDA) over a 3 month period of March 18 2024 -> June 18 2024.

![image unavailable](https://github.com/annaw3558/data-analysis-projects/blob/main/2.%20Basic%20Stock%20Analysis/img/img_1.png?raw=true)
*1. Recorded close price for each stock in a line graph.*

![image unavailable](https://github.com/annaw3558/data-analysis-projects/blob/main/2.%20Basic%20Stock%20Analysis/img/img_2.png?raw=true)
*2.  Recorded close price for each stock in an area graph. We can also better see and compare the overall stock performance in the given time period.*

![image unavailable](https://github.com/annaw3558/data-analysis-projects/blob/main/2.%20Basic%20Stock%20Analysis/img/img_3.png?raw=true)
*3. Closing price **(blue)**, 10 day moving average **(red)**, and 20 day moving average **(green)** for each stock. Moving averages can be used to help determine the direction of a stock trend by smoothing out volatility of the day-over-day movement of the stock.*

![image unavailable](https://github.com/annaw3558/data-analysis-projects/blob/main/2.%20Basic%20Stock%20Analysis/img/img_4.png?raw=true)
*4. Stock volatility shown by calculating the standard deviation of close prices. We use the default formula by dividing by n-1*

![image unavailable](https://github.com/annaw3558/data-analysis-projects/blob/main/2.%20Basic%20Stock%20Analysis/img/img_5.png?raw=true)
*5. Correlation graph between Nvidia and Microsoft close price, using ordinary least squares (OLS) to display a regression trendline.*


### Key Takeaways
1. Microsoft has the highest close price out of all stocks
1. Nvidia and Google saw volatility in their stock performance around April 30th. Nvidia again saw a second wave of volatility around June 1. Looking at closing prices, Google saw a surge in close cost while Nvidia saw a small drop followed by rapid growth.
1. We can see there is a correlation between Nvidia and Microsoft close prices. This can be explained by both companies being in similar industries, but overall the relationship isn't very strong.

Hope you enjoyed this small analysis - I did!!