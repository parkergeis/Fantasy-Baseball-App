# Fantasy DB - Overall Ranks

# Add champions, overall win %
# Add maybe some cool visuals

import streamlit as st
import pandas as pd
import datetime
today = datetime.date.today()
year = today.year

st.set_page_config(
    page_title="Fantasy Dashboard",
    layout="wide")

# Import data - needs manually uploaded and committed to GitHub
Standings = pd.read_excel('data/FantasyData.xlsx', sheet_name='PreviousStandings')
Standings['Record'] = Standings['Wins'].astype(str) + '-' + Standings['Losses'].astype(str) + '-' + Standings['Ties'].astype(str)
Champs = Standings[(Standings['Rank'] == 1) & (Standings['Year'] != year)]
Champs['Year'] = Champs['Year'].astype(str)

col = st.columns((1, 1), gap='medium')
with col[0]:
    st.markdown('<h3 style="text-align: center;">Champions</h3>', unsafe_allow_html=True)
    st.dataframe(Champs, column_order=['Year', 'Team', 'Owner', 'Record'], hide_index=True)



