'''
coding:utf-8
@Software:PyCharm
@Time:2024/1/13 12:47
@Author:Super Cao
'''
import datetime
import time
import alpaca_trade_api as tradeapi
import numpy as np
import pandas as pd
from datetime import timedelta
from pytz import timezone
import logging
import streamlit as st

pd.options.display.max_rows = 999
pd.set_option('display.max_columns', None)
tz = timezone('EST')
API_KEY = "PKYYODA53HBGXJQ79IBD"
SECRET_KEY = "irsQqeKqjbX1L9TiU5rueGVamiV6YLIAxHoPzfRy"
api = tradeapi.REST(API_KEY,
                    SECRET_KEY,
                    'https://paper-api.alpaca.markets')
# ----Frequency to check-----#
freq = '1Min'
# ----Moving average-----#
slow = 10
fast = 1


# loading = {'AAPL': 300, 'TSLA': 300}  # record the volume of each ticker


def simulate_market_clock(start_date):
    market_open_time = datetime.datetime.strptime(start_date.strftime('%Y-%m-%d') + ' 09:30:00', '%Y-%m-%d %H:%M:%S')
    market_close_time = datetime.datetime.strptime(start_date.strftime('%Y-%m-%d') + ' 16:00:00', '%Y-%m-%d %H:%M:%S')
    current_time = market_open_time

    while current_time <= market_close_time:
        current_time += timedelta(seconds=60 * 20)
        open_time = market_open_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        time_now = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        # yield current_time.strftime('%Y-%m-%dT%H:%M:%S-05:00')
        yield market_open_time, current_time

        # time.sleep(1)


def get_data_bars(symbols, loading, rate, slow, fast, start, end):
    """
    Return the historical data of a set of stocks
    :param symbols: tickers
    :param rate:
    :param slow:
    :param fast:
    :return:
    """
    # establish log to record each trade #
    logging.basicConfig(filename='log/{}.log'.format(time.strftime("%Y%m%d")))
    logging.warning('{} logging started'.format(datetime.datetime.now().strftime("%x %X")))
    # merge all the data

    # create the dataframe through API #
    st.write('Fetching data...')
    print('Fetching data...')
    try:
        # end = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=15)).strftime(
        #     '%Y-%m-%dT%H:%M:%SZ')
        raw_df = api.get_bars(symbols, timeframe=rate, limit=20 * len(symbols), adjustment="raw", start=start,
                              end=end).df

        # concat method
        single_dfs = {}
        for s in symbols:
            single_dfs[s] = raw_df.loc[raw_df['symbol'] == s, :].drop('symbol', axis=1)
        data = pd.concat(single_dfs.values(), axis=1, keys=single_dfs.keys())

        # ticker, qty, avg_entry_price are code, quantity, price when buying respectively #
        ticker = [x.symbol for x in api.list_positions()]
        qty = [x.qty for x in api.list_positions()]
        avg_entry_price = [x.avg_entry_price for x in api.list_positions()]
        my_position = dict(zip(ticker, qty))
        entry_price = dict(zip(ticker, avg_entry_price))

        # fast_ema_1min average in one minute #
        # slow_ema_10min average of past 10 minutes
        # return_1_min return of past one minute
        # loading buying volume
        # PL profit and loss #
        # for x in (list(loading.keys())):
        for x in symbols:
            data.loc[:, (x, 'fast_ema_1min')] = data[x]['close'].rolling(window=fast).mean()
            data.loc[:, (x, 'slow_ema_10min')] = data[x]['close'].rolling(window=slow).mean()
            data.loc[:, (x, 'return_1_min')] = (data[x]['close'] - data[x]['close'].shift(1)) / (
                data[x]['close'].shift(1))
            data.loc[:, (x, 'diff')] = data[x]['slow_ema_10min'] - data[x]['fast_ema_1min']
            data.loc[:, (x, 'loading')] = int(loading[x])

            if x in ticker:
                data.loc[:, (x, 'qty')] = int(my_position[x])
                data.loc[:, (x, 'entry_price')] = float(entry_price[x])
            else:
                data.loc[:, (x, 'qty')] = 0
                data.loc[:, (x, 'entry_price')] = data[x]['close']
            data.loc[:, (x, 'PL')] = (data[x]['close'] - data[x]['entry_price']) * (data[x]['qty'])

        data.fillna(method='ffill', inplace=True)
        print("Download the selected symbols successfully")
        st.write("Download the selected symbols successfully")
        return data
    except:
        st.write("There might be connection errors")
        print("There might be connection errors")
        pass


def get_signal_bars(symbol_list, loading, rate, ema_slow, ema_fast, start, end):
    """
    yield signals for trading, here is the specific strategy adopted
    :param symbol_list:
    :param rate:
    :param ema_slow:
    :param ema_fast:
    :return:
    """
    now = datetime.datetime.now()
    data = get_data_bars(symbol_list, loading, rate, ema_slow, ema_fast, start, end)
    signals = {}
    for x in symbol_list:
        # BUY when fma > sma #
        if (data[x].iloc[-1]['fast_ema_1min'] >= data[x].iloc[-1]['slow_ema_10min']):
            signal = (data[x].iloc[-1]['loading'])

        # SELL/Liquidation when fma < sma #
        else:
            signal = (data[x].iloc[-1]['qty']) * (-1)
        signals[x] = signal

    return signals


def time_to_open(current_time):
    """
    return the time left till the market is open
    :param current_time:
    :return:
    """
    if current_time.weekday() <= 4:
        d = (current_time + timedelta(days=1)).date()
    else:
        days_to_mon = 0 - current_time.weekday() + 7
        d = (current_time + timedelta(days=days_to_mon)).date()
    next_day = datetime.datetime.combine(d, datetime.time(9, 30, tzinfo=tz))
    seconds = (next_day - current_time).total_seconds()
    return seconds


# main trading function
def run_checker(stocklist, amount_dict, date):
    """
    execute the strategy and print trading information
    :param stocklist:
    :param amount_dict:
    :param date:
    :return:
    """

    print('HFT started!')
    st.text('HFT started!')
    clock = simulate_market_clock(date)
    while True:
        # Check if Monday-Friday #
        open_time, time_now = next(clock)
        # if datetime.datetime.now(tz).weekday() >= 0 and datetime.datetime.now(tz).weekday() <= 4:
        if time_now.weekday() >= 0 and time_now.weekday() <= 4:
            # Checks market is open #
            st.write('Trading in process ' + datetime.datetime.now().strftime("%x %X"))
            # print('Trading in process ' + datetime.datetime.now().strftime("%x %X"))
            print('Trading in process ' + time_now.strftime("%x %X"))
            # if datetime.datetime.now(tz).time() > datetime.time(9, 30) and datetime.datetime.now(
            #         tz).time() <= datetime.time(16, 00):
            if time_now.time() > datetime.time(9, 30) and time_now.time() <= datetime.time(16, 00):
                signals = get_signal_bars(stocklist, amount_dict, freq, slow, fast,
                                          open_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                                          time_now.strftime('%Y-%m-%dT%H:%M:%SZ'))
                for signal in signals:
                    if signals[signal] > 0:
                        # BUY
                        try:
                            api.submit_order(signal, signals[signal], 'buy', 'market', 'day')
                            print('{} bought {}  {} shares, portfolio value {}   '.format(
                                datetime.datetime.now(tz).strftime("%x %X"), signal, signals[signal],
                                api.get_account().equity))
                            st.write('{} bought {}  {} shares, portfolio value {}   '.format(
                                datetime.datetime.now(tz).strftime("%x %X"), signal, signals[signal],
                                api.get_account().equity))
                            # BUY #
                            logging.warning('{} bought {}  {} shares, portfolio value {}   '.format(
                                datetime.datetime.now(tz).strftime("%x %X"),
                                signal, signals[signal], api.get_account().equity))
                        except:
                            # not enough buying power#
                            logging.warning(
                                '{} Insufficient buying power'.format(datetime.datetime.now(tz).strftime("%x %X")))
                            print('Trading in process ' + datetime.datetime.now().strftime(
                                "%x %X") + ' buying ' + signal + ' but Insufficient fund')
                            st.write('Trading in process ' + datetime.datetime.now().strftime(
                                "%x %X") + ' buying ' + signal + ' but Insufficient fund')
                            pass
                    elif signals[signal] < 0:
                        try:
                            api.submit_order(signal, -signals[signal], 'sell', 'market', 'day')
                            print('{} sold   {} {} shares, portfolio value {}   '.format(
                                datetime.datetime.now(tz).strftime("%x %X"), signal, signals[signal],
                                api.get_account().equity))
                            st.write('{} sold   {} {} shares, portfolio value {}   '.format(
                                datetime.datetime.now(tz).strftime("%x %X"), signal, signals[signal],
                                api.get_account().equity))
                            # SELL #
                            logging.warning('{} sold   {} {} shares, portfolio value {}   '.format(
                                datetime.datetime.now(tz).strftime("%x %X"), signal, signals[signal],
                                api.get_account().equity))
                        except Exception as e:
                            pass
                        # rest for one minute #
                time.sleep(5)

            else:
                # print Warning message #
                print('Market closed ({})'.format(datetime.datetime.now(tz)))
                print('Sleeping', round(time_to_open(datetime.datetime.now(tz)) / 60 / 60, 2), 'hours')
                time.sleep(time_to_open(datetime.datetime.now(tz)))
        else:
            # print Warning message #
            st.text('Market closed ({})'.format(datetime.datetime.now(tz)))
            st.text('Sleeping', round(time_to_open(datetime.datetime.now(tz)) / 60 / 60, 2), 'hours')
            print('Market closed ({})'.format(datetime.datetime.now(tz)))
            print('Sleeping', round(time_to_open(datetime.datetime.now(tz)) / 60 / 60, 2), 'hours')
            time.sleep(time_to_open(datetime.datetime.now(tz)))

# test
# data = get_data_bars(list(loading.keys()), freq, slow, fast)
# run_checker(list(loading.keys()), datetime.datetime(2024, 1, 12))
