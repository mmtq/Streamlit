import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


st.title('NFL Football Player Stats Explorer')

st.markdown("""
This app performs simple webscraping of NFL Football player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [pro-football-reference.com](https://www.pro-football-reference.com/).
""")


st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1960, 2025))))

# Web scraping of NFL player stats
@st.cache_data
def load_data(year):
    url = "https://www.pro-football-reference.com/years/"+str(year)+"/rushing.htm"
    html = pd.read_html(url, header = 1)
    df = html[0]
    df = df.drop(df[df.Age=='Age'].index)
    df.index = range(1, len(df)+1)
    df = df.drop(['Rk'], axis=1)
    df = df.dropna(subset=['Pos', 'Tm'])
    df = df.fillna(0)
    return df

player_stats = load_data(selected_year)
# player_stats
# Sidebar - Team selection
sorted_unique_team = sorted(player_stats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position Selection
sorted_unique_position = sorted(player_stats.Pos.astype(str).unique())
selected_position = st.sidebar.multiselect('Position', sorted_unique_position, sorted_unique_position)

# Filtering data

df_data = player_stats[(player_stats.Tm.isin(selected_team)) & (player_stats.Pos.isin(selected_position))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_data.shape[0]) + ' rows and ' + str(df_data.shape[1]) + ' columns.')
st.dataframe(df_data)

# Heatmap

if st.button('Intercorrelation Heatmap'):
    df_data = df_data.apply(pd.to_numeric, errors='coerce')
    
    numeric_df = df_data.select_dtypes(include=['float64', 'int64'])
    
    # if not numeric_df.empty:
    corr = numeric_df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True, annot=True, cmap="coolwarm")
        st.pyplot(f)
    # else:
    #     st.write("No numeric data available for correlation heatmap.")
        

