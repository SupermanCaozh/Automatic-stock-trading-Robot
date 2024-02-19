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
The user could get access to the High-Frequency Trading Robot by clicking the red button with text High-frequency Algorithmic Trading once. Users can select a set of stocks by entering their tickers as well as the amount to buy once there is a buy signal is triggered. Users can also change the particular trading day to any other date when the U.S. market is open. A Moving Average trading strategy is adopted in this intraday trading application. The strategy is implemented by clicking the red button on the sidebar with text Start simulating intraday trading in a single day.
Once the strategy is launched, the system interface will scroll and print out transaction records every ten minutes (if the buy or sell signal is
triggered), and automatically submit a transaction request through the Alpaca API. Since Alpaca users of a free plan cannot obtain real-time updated live data on the current date, we select minute-level historical data of a certain trading day in the past, which can be modified if you have an advanced account. And we created a virtual clock to simulate the passage of time in real life. The following figures showed an illustration of the trading record in a random day with flash every 10 minutes.
![image](https://github.com/SupermanCaozh/Streamlit-Automatic-Stock-Trading-Robot/assets/96049887/05eddc59-0331-45e6-a4a0-fbca9eb82fb1)![image](https://github.com/SupermanCaozh/Streamlit-Automatic-Stock-Trading-Robot/assets/96049887/869323bd-84a5-4d15-ab66-471d0c3627d4)






