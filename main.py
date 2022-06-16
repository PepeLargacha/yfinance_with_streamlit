import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
import pandas as pd


# Title and subtitle for the app
st.write("""
# Simple Price App

Showing candlesticks for BTC-USD.
""")

# Get the data from yfinance
tickersymbol = 'BTC-USD'
tickerdata = yf.Ticker(tickersymbol)
ticker_df = tickerdata.history(period='2mo', interval='1h', actions=False)

# Plot the candlesticks
figure = go.Figure(
    data=[
          go.Candlestick(
            x=ticker_df.index,
            low=ticker_df['Low'],
            high=ticker_df['High'],
            open=ticker_df['Open'],
            close=ticker_df['Close'],
            name='Candlesticks'
          )
    ])
figure.update_layout(xaxis_rangeslider_visible=False)

st.write(figure)
