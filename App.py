'''
coding:utf-8
@Software:PyCharm
@Time:2024/1/10 12:01
@Author:Super Cao
'''

import streamlit as st
from matplotlib import pyplot as plt
import datetime

from metrics import plot_metrics
import Strategy
from Strategy import *

import threading


def dashboard():
    st.title('🔱A Qua -- Dashboard')

    if st.button("High-frequency Algorithmic Trading", type="primary"):
        st.session_state.page_number += 1
        st.experimental_rerun()

    ticker = st.sidebar.text_input('Please pick up a stock by its ticker', value='AAPL')
    today = datetime.datetime.now()
    one_week_ago = today - datetime.timedelta(days=252)
    start = st.sidebar.date_input('When do you want to start form', value=one_week_ago, format="YYYY/MM/DD")
    end = st.sidebar.date_input('When do you want to end at', value='today')
    bb_period = st.sidebar.number_input('Please choose a moving average period for Bollinger Bands', value=20)
    # rsi_period = st.sidebar.number_input('Please choose a moving average period for RSI', value=14)

    # plot the metics
    fig_main, fig_metrics = plot_metrics(ticker, start, end, bb_period)

    st.plotly_chart(fig_main)
    st.plotly_chart(fig_metrics)


def trading():
    st.title('🔱A Qua -- A Quant Trading Platform')

    button_trade = st.sidebar.button("Start simulating intraday trading in a single day", type="primary")

    if st.button("My Dashboard", type="primary"):
        st.session_state.page_number -= 1
        st.experimental_rerun()

    # return the ticker list
    stock_list = st.sidebar.text_input("Select the stocks interested (seperated by a comma)", value="AAPL,TSLA")
    amount_list = st.sidebar.text_input("Enter the amount to buy once a buy signal is triggered", value="300,600")
    st.sidebar.write("List of the stocks selected")
    stock_list = stock_list.split(',')
    amount_list = amount_list.split(',')
    amount_dict = dict(zip(stock_list, amount_list))
    date = st.sidebar.date_input('Choose a weekday to simulate intraday trading', value=datetime.date(2024, 1, 12),
                                 format="YYYY/MM/DD")
    for stock in stock_list:
        st.sidebar.write(f"{stock}")

    if button_trade:
        run_checker(stock_list, amount_dict, date)


if 'page_number' not in st.session_state:
    st.session_state.page_number = 1
if st.session_state.page_number == 1:
    dashboard()
elif st.session_state.page_number == 2:
    trading()
