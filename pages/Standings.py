# Fantasy DB - Standings

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
Curr['GB'] = Curr['Points'].max() - Curr['Points']
Prev['Year'] = Prev['Year'].astype(str)
Curr['Year'] = Curr['Year'].astype(str)
Champs = Standings[(Standings['Rank'] == 1) & (Standings['Year'] != year)]
Champs['Year'] = Champs['Year'].astype(str)

def highlight_champs(s):
    return ['color: gold' for _ in s]

# Apply the style to the DataFrame
styled_Champs = Champs.style.apply(highlight_champs)

col = st.columns((1, 5, 1), gap='medium')
with col[1]:
    st.markdown('<h3 style="text-align: center;">🏆Champions🏆</h3>', unsafe_allow_html=True)
    st.dataframe(styled_Champs, column_order=['Year', 'Team', 'Owner', 'Record'], hide_index=True, width=3000) 
col = st.columns((1.1, 1), gap='medium')
with col[0]:
    st.markdown('<h3 style="text-align: center;">Current Standings</h3>', unsafe_allow_html=True)
    st.dataframe(Curr, hide_index=True, width = 600, column_order=['Rank', 'Team', 'Owner', 'Record', 'GB'])
with col[1]:
    st.markdown('<h3 style="text-align: center;">Previous Standings</h3>', unsafe_allow_html=True)
    st.dataframe(Prev, hide_index=True, width=1000, column_order=['Year', 'Rank', 'Team', 'Owner', 'Record'])


