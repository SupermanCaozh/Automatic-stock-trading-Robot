# Automatic-stock-trading-Robot
US stock intraday automatic trading platform based on MA strategy

## Brief Introduction
### Dashboard
This project provides a quantitative trading platform for intraday trading in the U.S. stock market. Leveraging the Alpaca virtual trading platform’s API, it aims to automatically execute strategies for buying or liquidating through algorithms. The name of the quantitative trading platform is A Qua, which is not only an acronym of A Quantitative Trading Platform but also that of Aquaman (although I am not a big fan of DC... Viva la Marvel!).

We utilize the Alpaca trading platform’s API to retrieve data and conduct virtual trading (Paper trading). The trading process does not require logging into
the Alpaca platform or manual intervention. It is entirely automated through our application interface.

The first page of this application is a dashboard which displays the plot of several important and common indicators of a single selected ticker over a particular time period. The dashboard displays, in this version, five figures or indicators which are computed in the metrics.py including Candlestick, Bollinger Bands, Relative Strength Index (RSI), Volume and Return and Moving Average Convergence/Divergence indicator (MACD). The following figure shows the interface of the dashboard.
![image](https://github.com/SupermanCaozh/Streamlit-Automatic-Stock-Trading-Robot/assets/96049887/d6cdc816-ace4-48da-a4ce-dc59479c318b)![image](https://github.com/SupermanCaozh/Streamlit-Automatic-Stock-Trading-Robot/assets/96049887/79a65f4c-82a7-407d-990c-1177abb02680)
### Trading Robot
The user could get access to the High-Frequency Trading Robot by clicking the red button with text High-frequency Algorithmic Trading once. Users can select a set of stocks by entering their tickers as well as the amount to buy once there is a buy signal is triggered. Users can also change the particular trading day to any other date when the U.S. market is open





