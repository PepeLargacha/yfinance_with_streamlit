from datetime import datetime
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
import pandas as pd


# Title and subtitle for the app
st.write("""
# Simple Price App

Showing candlesticks for BTC-USD.
""")

st.sidebar.header("User Input")
tickersymbol = st.sidebar.text_input("Ticker Symbol", "BTC-USD")
from_date = st.sidebar.date_input("From", value=pd.Timestamp('2021-01-01'))
to_date = st.sidebar.date_input("To", value=pd.Timestamp(datetime.today()))
interval = st.sidebar.selectbox("Interval", ["1h", "1d", '1wk', '1mo'])

# Get the data from yfinance
tickerdata = yf.Ticker(tickersymbol)
ticker_df = tickerdata.history(start=from_date, end=to_date, interval=interval, actions=False)

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
