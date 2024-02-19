'''
coding:utf-8
@Software:PyCharm
@Time:2024/1/10 13:20
@Author:Super Cao
'''
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ta
import numpy as np


def plot_metrics(ticker, start_date, end_date, bb_period):
    # download the data of ticker
    df = yf.download(ticker, start_date, end_date)
    df['ma_mean'] = df.Close.rolling(bb_period).mean()
    df['ma_std'] = df.Close.rolling(bb_period).std()
    df['upper_bb'] = df.ma_mean + 2 * df.ma_std
    df['lower_bb'] = df.ma_mean - 2 * df.ma_std
    df_momentum = ta.add_momentum_ta(df, 'High', 'Low', 'Close', 'Volume')
    df['rsi'] = df_momentum['momentum_rsi']
    df['stoch_rsi'] = df_momentum['momentum_stoch_rsi']
    df['stoch_rsi_k'] = df_momentum['momentum_stoch_rsi_k']
    df['stoch_rsi_d'] = df_momentum['momentum_stoch_rsi_d']
    df['return'] = df['Close'].pct_change()
    df['log_ret'] = np.log(df.Close) - np.log(df.Close.shift(1))
    # calculate MACD
    short_term = 12
    long_term = 26
    signal_period = 9
    short_ema = df['Close'].ewm(span=short_term, adjust=False).mean()
    long_ema = df['Close'].ewm(span=long_term, adjust=False).mean()
    macd_line = short_ema - long_ema
    # signal line
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    macd_histogram = macd_line - signal_line
    df['MACD'] = macd_line
    df['Signal'] = signal_line
    df['Histogram'] = macd_histogram

    fig_main = make_subplots(rows=1, cols=1,
                             subplot_titles=[f'Candlestick of {ticker}'])

    # Candlestick
    fig_main.add_trace(go.Candlestick(x=list(df.index),
                                      open=df.Open,
                                      close=df.Close,
                                      high=df.High,
                                      low=df.Low, showlegend=False,
                                      name="candlestick"),
                       row=1, col=1)

    fig_metrics = make_subplots(rows=4, cols=1, shared_xaxes=True,
                                subplot_titles=(
                                    'Bollinger Bands', 'Relative Strength Index', 'Log Return and Daily Volume',
                                    'MACD'),
                                vertical_spacing=0.05,
                                specs=[[{'secondary_y': False}], [{'secondary_y': True}], [{'secondary_y': True}],
                                       [{'secondary_y': False}]]
                                )
    # bb
    fig_metrics.add_trace(go.Scatter(x=list(df.index),
                                     y=df['Close'],
                                     line_color='red', name="closing price", showlegend=False), row=1, col=1)

    fig_metrics.add_trace(go.Scatter(x=list(df.index),
                                     y=df['ma_mean'],
                                     line_color="pink", line={'dash': 'dash'}, name="moving average with window 20",
                                     showlegend=False), row=1,
                          col=1)

    fig_metrics.add_trace(go.Scatter(x=list(df.index),
                                     y=df['upper_bb'],
                                     line_color="skyblue", line={'dash': 'dash'}, name="upper bollinger band",
                                     showlegend=False), row=1, col=1)
    fig_metrics.add_trace(go.Scatter(x=list(df.index),
                                     y=df['lower_bb'],
                                     line_color="darkblue", line={'dash': 'dash'}, name="lower bollinger band",
                                     showlegend=False), row=1,
                          col=1)

    # rsi
    fig_metrics.add_trace(go.Scatter(x=list(df.index),
                                     y=df['rsi'],
                                     line_color='blue',
                                     name='RSI',
                                     showlegend=False), row=2, col=1)
    fig_metrics.add_trace(go.Scatter(x=list(df.index),
                                     y=df['stoch_rsi'],
                                     line_color='skyblue',
                                     showlegend=False), secondary_y=True, row=2, col=1)
    fig_metrics.add_trace(go.Scatter(x=list(df.index),
                                     y=df['stoch_rsi_k'],
                                     line_color='pink',
                                     showlegend=False), secondary_y=True, row=2, col=1)
    fig_metrics.add_trace(go.Scatter(x=list(df.index),
                                     y=df['stoch_rsi_d'],
                                     line_color='purple',
                                     showlegend=False), secondary_y=True, row=2, col=1)

    # Volume and Return
    fig_metrics.add_trace(go.Scatter(x=list(df.index),
                                     y=df['log_ret'],
                                     showlegend=False, fill='tozeroy'), row=3, col=1)
    fig_metrics.add_trace(go.Scatter(x=list(df.index),
                                     y=df['Volume'],
                                     showlegend=False, fill='tonexty'), secondary_y=True, row=3, col=1)
    fig_metrics.layout['xaxis'].update(rangebreaks=[{'pattern': 'day of week', 'bounds': [6, 1]}])

    # MACD
    fig_metrics.add_trace(go.Scatter(x=df.index, y=df['MACD'], mode='lines', name='MACD', showlegend=False), row=4,
                          col=1)
    fig_metrics.add_trace(go.Scatter(x=df.index, y=df['Signal'], mode='lines', name='Signal', showlegend=False), row=4,
                          col=1)
    fig_metrics.add_trace(go.Bar(x=df.index, y=df['Histogram'], name='Histogram',
                                 marker_color=['green' if val >= 0 else 'red' for val in df['Histogram']],
                                 showlegend=False), row=4, col=1)
    fig_metrics.update_layout(
        title_text='Subplots with Different metrics',
        height=800
    )

    return fig_main, fig_metrics
