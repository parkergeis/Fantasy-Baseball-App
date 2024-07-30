# Fantasy DB - Rosters

# Add reset filters button
# Add savant metrics, not just visual
# Add statistics filter (numeric, percentiles, etc)
# Add drill down to bref, statcast, fgraphs with links

import streamlit as st
import pandas as pd
import pybaseball as pyb
import unidecode

st.set_page_config(
    page_title="Fantasy Dashboard",
    layout="wide",
    initial_sidebar_state="auto")

# Import data - needs manually uploaded and committed to GitHub
Rosters = pd.read_excel('data/FantasyData.xlsx', sheet_name='Rosters')
Rosters['Year'] = Rosters['Year'].astype(str)

# Filters
with st.sidebar:  
    def reset_filters():
            st.session_state.team = "1All"
            st.session_state.player = "1All"
            st.session_state.year = "1All"
            selected_team = '1All'
            selected_player = '1All'
            selected_year = '1All'
            selectedRosters = Rosters
    st.button('Reset Filters', on_click=reset_filters)
    
    team_list = list(Rosters.Owner.unique())[::-1]
    team_list.append('1All')
    team_list.sort()
    selected_team = st.selectbox('Team', team_list, index=0, key='team')
    if selected_team == '1All':
        selectedRosters = Rosters
    else:
        selectedRosters = Rosters[Rosters.Owner == selected_team]

    player_list = list(selectedRosters.Player.unique())[::-1]
    player_list.append('1All')
    player_list.sort()
    selected_player = st.selectbox('Player', player_list, index=0, key='player')
    if selected_player == '1All':
        selectedRosters = selectedRosters
    else:
        selectedRosters = selectedRosters[selectedRosters.Player == selected_player]  
    
    year_list = list(selectedRosters.Year.unique())[::-1]
    year_list.append('1All')
    year_list.sort()
    selected_year = st.selectbox('Year', year_list, index=0, key='year')
    if selected_year == '1All':
        selectedRosters = selectedRosters
    else:
        selectedRosters = selectedRosters[selectedRosters.Year == selected_year]  

# If player/year is selected, pull Savant data
savant = False
hitter = False
pitcher = False
if (selected_player != '1All') and (selected_year != '1All'):
    savant = True
    hitter_ranks = pyb.statcast_batter_percentile_ranks(selected_year)
    hitter_ranks = hitter_ranks[['player_name', 'xwoba', 'xba', 'xslg', 'exit_velocity', 'brl_percent', 'hard_hit_percent', 'bat_speed', 'chase_percent', 'whiff_percent', 'k_percent', 'bb_percent']]
    hitter_ranks.columns = ['Name', 'xwOBA', 'xBA', 'xSLG', 'Exit Velocity', 'Barrel %', 'Hard-Hit %', 'Bat Speed', 'Chase %', 'Whiff %', 'K %', 'BB %']
    hitter_ranks['Name'] = hitter_ranks['Name'].apply(lambda x: unidecode.unidecode(x) if isinstance(x, str) else x)
    hitter_ranks[['last_name', 'first_name']] = hitter_ranks['Name'].str.split(',', expand=True).apply(lambda x: x.str.strip())
    hitter_ranks['Name'] = hitter_ranks['first_name'] + " " + hitter_ranks['last_name']
    hitter_ranks.drop(['first_name', 'last_name'], axis=1, inplace=True)
    hitter_ranks = hitter_ranks[hitter_ranks['Name'] == selected_player]
    hitter_ranks = hitter_ranks.melt(id_vars=['Name'], var_name='stat', value_name='value')

    pitcher_ranks = pyb.statcast_pitcher_percentile_ranks(selected_year)
    pitcher_ranks = pitcher_ranks[['player_name', 'xera', 'xba', 'fb_velocity', 'exit_velocity', 'chase_percent', 'whiff_percent', 'k_percent', 'bb_percent', 'brl_percent', 'hard_hit_percent']]
    pitcher_ranks.columns = ['Name', 'xERA', 'xBA', 'Fastball Velocity', 'Exit Velocity', 'Chase %', 'Whiff %', 'K %', 'BB %', 'Barrel %', 'Hard-Hit %']
    pitcher_ranks['Name'] = pitcher_ranks['Name'].apply(lambda x: unidecode.unidecode(x) if isinstance(x, str) else x)
    pitcher_ranks[['last_name', 'first_name']] = pitcher_ranks['Name'].str.split(',', expand=True).apply(lambda x: x.str.strip())
    pitcher_ranks['Name'] = pitcher_ranks['first_name'] + " " + pitcher_ranks['last_name']
    pitcher_ranks.drop(['first_name', 'last_name'], axis=1, inplace=True)
    pitcher_ranks = pitcher_ranks[pitcher_ranks['Name'] == selected_player]
    pitcher_ranks = pitcher_ranks.melt(id_vars=['Name'], var_name='stat', value_name='value')

    if not hitter_ranks.empty:
        hitter = True
    if not pitcher_ranks.empty:
        pitcher = True

col = st.columns((1, 1), gap='medium')
with col[0]:
    st.markdown('<h3 style="text-align: left;">Rosters</h3>', unsafe_allow_html=True)
    st.dataframe(selectedRosters, hide_index=True, width=900)

if savant:
    with col[1]:
        st.markdown('<h3 style="text-align: left;">Percentile Ranks</h3>', unsafe_allow_html=True)
        if hitter:
            st.dataframe(hitter_ranks,
                    column_order=("stat", 'value'),
                    hide_index=True,
                    width=350,
                    height=422,
                    column_config={
                    "Player": st.column_config.TextColumn(
                        "Player",
                    ),
                    "stat": st.column_config.TextColumn(
                        "Stat",
                    ),
                    "value": st.column_config.ProgressColumn(
                        "",
                        format="%f",
                        min_value=0,
                        max_value=100,
                        )}
                    )
        if pitcher:
            st.dataframe(pitcher_ranks,
                    column_order=("stat", 'value'),
                    hide_index=True,
                    width=350,
                    height=388,
                    column_config={
                    "Player": st.column_config.TextColumn(
                        "Player",
                    ),
                    "stat": st.column_config.TextColumn(
                        "Stat",
                    ),
                    "value": st.column_config.ProgressColumn(
                        "",
                        format="%f",
                        min_value=0,
                        max_value=100,
                        )}
                    )
else: 
    with col[1]:
        st.markdown('<h3 style="text-align: center;">Select a player and year combination to see statistics!</h3>', unsafe_allow_html=True)


