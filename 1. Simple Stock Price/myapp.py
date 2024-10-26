import yfinance as yf
import streamlit as st
import pandas as pd


st.write("""
# Simple Stock Price App
""")
usr_inp = st.text_input("Enter tickerSymbol (e.g. 'GOOGL', 'AAPL') ")

tickerSymbol = usr_inp.strip()

if(tickerSymbol):
    st.write("""
    Shown are the stock closing price and volume for the selected tickerSymbol!
    """)

    tickerData =  yf.Ticker(tickerSymbol)

    tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2024-5-31')

    st.write("""
    ## Open
    """)
    st.line_chart(tickerDf.Open)
    st.write("""
    ## Close
    """)

    st.line_chart(tickerDf.Close)
    st.write("""
    ## Volume
    """)

    st.line_chart(tickerDf.Volume)
