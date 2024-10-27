import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

st.title('NBA Player Stats Explorer')

st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit 
* **Data source:** [basketball-reference.com](https://www.basketball-reference.com/).
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950, 2024))))

# Web scraping of NBA player stats
@st.cache_data
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_totals.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    # df['Age'] = df['Age'].astype(str)
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    raw = raw.drop(raw[raw.Age == 0].index)
    player_stats = raw.drop(['Rk'], axis=1)
    player_stats = player_stats.drop('Awards', axis=1)
    return player_stats

player_stats = load_data(selected_year)
# player_stats

#Sidebar - Team selection
sorted_unique_team = sorted(player_stats.Team.astype(str).unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
sorted_unique_position = sorted(player_stats.Pos.astype(str).unique())
selected_postion = st.sidebar.multiselect('Position', sorted_unique_position, sorted_unique_position)

# Filtering data
df_selected_team = player_stats[(player_stats.Team.isin(selected_team)) & (player_stats.Pos.isin(selected_postion))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimenstion: '+ str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

# Heatmap

if st.button('Intercorrelation Heatmap'):
# Select only the numeric columns in df_selected_team for correlation calculation
    numeric_df = df_selected_team.select_dtypes(include=['float64', 'int64'])
    corr = numeric_df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(f)

