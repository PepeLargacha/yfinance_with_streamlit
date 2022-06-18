from datetime import datetime
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots as mksub
import pandas as pd

pd.options.plotting.backend = "plotly"
# Create a sidebar with filters for the data
st.sidebar.header("Filters")
tickersymbol = st.sidebar.text_input("Ticker Symbol", "BTC-USD").upper()
from_date = st.sidebar.date_input("From", value=pd.Timestamp('2022-01-01'))
to_date = st.sidebar.date_input("To", value=pd.Timestamp(datetime.today()))
interval = st.sidebar.selectbox("Interval", ["1h", "1d", '1wk', '1mo'], index=1)

# App title
st.write("""
# Pricing App
""")

# Get the data from yfinance
tickerdata = yf.Ticker(tickersymbol)
ticker_df = tickerdata.history(start=from_date,
                               end=to_date,
                               interval=interval,
                               actions=False)

# Adding Moving Average to the dataframe
ticker_df['MA9'] = ticker_df['Close'].rolling(window=9, min_periods=0).mean()
ticker_df['MA21'] = ticker_df['Close'].rolling(window=21, min_periods=0).mean()
ticker_df['MA200'] = ticker_df['Close'].rolling(window=200, min_periods=0).mean()
ticker_df['VMA20'] = ticker_df['Volume'].rolling(window=20, min_periods=0).mean()

# Plot the candlesticks
figure = mksub(rows=2, cols=1, shared_xaxes=True,
               vertical_spacing=0, subplot_titles=("Price", "Volume"),
               row_width=[0.2, 0.7])

figure.add_trace(go.Candlestick(
                                x=ticker_df.index,
                                low=ticker_df['Low'],
                                high=ticker_df['High'],
                                open=ticker_df['Open'],
                                close=ticker_df['Close'],
                                name="Price",
                                increasing=dict(line=dict(color='#26a69a')),
                                decreasing=dict(line=dict(color='#ef5350'))),
                 row=1, col=1)

# Plot the moving average
figure.add_trace(go.Scatter(
                            x=ticker_df.index,
                            y=ticker_df['MA9'],
                            marker_color='#4caf50',
                            name="MA9"),
                 row=1, col=1)

figure.add_trace(go.Scatter(
                            x=ticker_df.index,
                            y=ticker_df['MA21'],
                            marker_color='#ffeb3b',
                            name="MA21"),
                 row=1, col=1)

figure.add_trace(go.Scatter(
                            x=ticker_df.index,
                            y=ticker_df['MA200'],
                            marker_color='brown',
                            name="MA200"),
                 row=1, col=1)

# Plot the volume  
figure.add_trace(go.Bar(
                        x=ticker_df.index,
                        y=ticker_df['Volume'],
                        name="Volume",
                        showlegend=False,
                        marker_color='red'),
                 row=2, col=1)

figure.update_layout(
    title=f"{tickersymbol}",
    xaxis_tickfont_size=12,
    yaxis_tickfont_size=12,
    autosize=False,
    width=800,
    height=600,
    margin=dict(l=50, r=50, b=100, t=100, pad=4),
    plot_bgcolor='#151924',)

figure.update(layout_xaxis_rangeslider_visible=False)


st.plotly_chart(figure)
