import streamlit as st
import yfinance as yf
import pandas as pd
import base64
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

st.title('S&P 500 Data Explorer')

st.markdown("""
This app performs simple webscraping of S&P 500 data!
* **Python libraries:** base64, pandas, streamlit 
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""")

@st.cache_data
def load_data():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

df = load_data()
# df

unique_sectors = sorted(set(df['GICS Sector']))
selected_sector = st.sidebar.multiselect('Sector', unique_sectors, unique_sectors)

df = df[(df['GICS Sector'].isin(selected_sector))]
selected_range = st.sidebar.slider('Number of Companies', 0, len(df)+1, (0, len(df)+1))
df = df.iloc[selected_range[0]:selected_range[1]]
# Show dataframe
st.header('S&P 500 Companies')
st.write('Data Dimension: ' + str(df.shape[0]) + ' rows and ' + str(df.shape[1]) + ' columns.')
st.dataframe(df)

st.markdown("""
## Show Stock Chart of Any Company
Here we can see the stock chart of any company.
""")

selected_company = st.text_input("Enter Company Symbol")

# @st.cache_data
if selected_company:
    company_data = yf.Ticker(selected_company)
    company_df = company_data.history(period='1d', start='2010-5-31', end='2024-5-31')
    st.header('Stock Chart of ' + selected_company)
    selected_chart = st.selectbox('Select Chart Type', ['Open', 'Close', 'High', 'Low'])
    st.line_chart(company_df[selected_chart])
    # st.line_chart(company_df.Open)