# Fantasy DB - Rosters

# Add reset filters button
# Add drill down to bref, statcast, fgraphs

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Fantasy Dashboard",
    layout="wide",
    initial_sidebar_state="auto")

# Import data - needs manually uploaded and committed to GitHub
Rosters = pd.read_excel('data/FantasyData.xlsx', sheet_name='Rosters')
Rosters['Year'] = Rosters['Year'].astype(str)

# Filters
with st.sidebar:  
    team_list = list(Rosters.Owner.unique())[::-1]
    team_list.append('1All')
    team_list.sort()
    selected_team = st.selectbox('Team', team_list, index=0)
    if selected_team == '1All':
        Rosters = Rosters
    else:
        Rosters = Rosters[Rosters.Owner == selected_team]

    player_list = list(Rosters.Player.unique())[::-1]
    player_list.append('1All')
    player_list.sort()
    selected_player = st.selectbox('Player', player_list, index=0)
    if selected_player == '1All':
        Rosters = Rosters
    else:
        Rosters = Rosters[Rosters.Player == selected_player]  
    
    year_list = list(Rosters.Year.unique())[::-1]
    year_list.append('1All')
    year_list.sort()
    selected_year = st.selectbox('Year', year_list, index=0)
    if selected_year == '1All':
        Rosters = Rosters
    else:
        Rosters = Rosters[Rosters.Year == selected_year]  

col = st.columns((1, 2, 1), gap='medium')
with col[1]:
    st.markdown('<h3 style="text-align: center;">Rosters</h3>', unsafe_allow_html=True)
    st.dataframe(Rosters, hide_index=True)



