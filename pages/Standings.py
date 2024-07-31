# Fantasy DB - Standings

# Add GB column

import streamlit as st
import pandas as pd
import datetime
today = datetime.date.today()
year = today.year

st.set_page_config(
    page_title="Fantasy Dashboard",
    layout="wide",
    initial_sidebar_state="auto")

# Import data - needs manually uploaded and committed to GitHub
Standings = pd.read_excel('data/FantasyData.xlsx', sheet_name='PreviousStandings')
Standings['Record'] = Standings['Wins'].astype(str) + '-' + Standings['Losses'].astype(str) + '-' + Standings['Ties'].astype(str)
Prev = Standings[Standings['Year'] != year]
Curr = Standings[Standings['Year'] == year]
Prev['Year'] = Prev['Year'].astype(str)
Curr['Year'] = Curr['Year'].astype(str)

col = st.columns((1, 1), gap='medium')
with col[0]:
    st.markdown('<h3 style="text-align: left;">Current Standings</h3>', unsafe_allow_html=True)
    st.dataframe(Curr, hide_index=True, column_order=['Rank', 'Team', 'Record'])
with col[1]:
    st.markdown('<h3 style="text-align: left;">Previous Standings</h3>', unsafe_allow_html=True)
    st.dataframe(Prev, hide_index=True, column_order=['Year', 'Rank', 'Team', 'Record'])


