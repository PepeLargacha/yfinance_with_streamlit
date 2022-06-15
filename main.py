import yfinance as yf
import streamlit as st
import pandas as pd

st.write("""
# Simple Stock Price App

Showing closing price and volume for Google
""")

tickersymbol = 'GOOGL'
tickerdata = yf.Ticker(tickersymbol)
ticker_df = tickerdata.history(period='1d', start='2010-5-31', end='2022-6-14')

st.line_chart(ticker_df.Close)
st.line_chart(ticker_df.Volume)
