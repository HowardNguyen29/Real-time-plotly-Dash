# Real-Time Candlestick Chart with RSI Indicator
This web application provides real-time candlestick charts with an integrated RSI (Relative Strength Index) indicator for popular cryptocurrency pairs (e.g., BTC/USD, ETH/USD, XRP/EUR). The app is built using Dash for the frontend and Plotly for data visualization, with live updates pulled from the Bitstamp API.

# Features:
+ Real-time Candlestick Chart: Displays real-time price movements (open, high, low, close) for selected cryptocurrency pairs.
+ RSI Indicator: Visualizes the Relative Strength Index (RSI) based on the closing price of the selected cryptocurrency pair.
+ Dynamic Controls: Users can choose the cryptocurrency pair, timeframe, and number of candlesticks displayed.
+ Real-time Updates: Data is refreshed every second to keep the charts up-to-date.
+ Range Slider: Allows the user to zoom in/out and adjust the range of displayed candlesticks.

# Technologies Used:
+ Python
+ Dash: Web framework for building interactive web applications.
+ Plotly: Library for interactive plotting and charting.
+ pandas: Data manipulation library for handling financial data.
+ pandas_ta: Technical analysis library for calculating the RSI.
+ Requests: HTTP library for fetching real-time data from the Bitstamp API.

# Usage
## Controls:
+ Coin: Select the cryptocurrency pair (BTC/USD, ETH/USD, XRP/EUR, etc.).
+ Timeframe: Choose the timeframe for each candlestick (e.g., 30 minutes, 1 hour, 1 day).
+ Num of Candlesticks: Choose how many candlesticks to display (e.g., 15, 25, 50).
+ Range Slider: Use the slider to zoom in or out on the chart, adjusting the range of candlesticks.
## Data Source:
+ The application fetches real-time data from the Bitstamp API (https://www.bitstamp.net/api/v2/ohlc/).
+ The RSI (Relative Strength Index) is calculated using pandas_ta (Technical Analysis library).
## Real-time Updates:
+ The app updates the charts every second using a dcc.Interval component. You can adjust the frequency by modifying the interval property in the Dash app.

# Screenshot
+ Here is the UI:
![image](https://github.com/user-attachments/assets/babe1ea0-7140-46c8-80d9-31cb92ec6a6f)

THANK YOU FOR YOUR READING!!
