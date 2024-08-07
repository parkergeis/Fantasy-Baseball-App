# Fantasy DB - Rosters

# Get rosters before playoff cuts? Not sure of possibility - try saving rosters before playoffs from now on
# New page to see MLB-wide stats and predictive stats (more freedom on filters)
# Add savant metrics, not just visual
# Formatting/spacing

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
            st.session_state.team = "All"
            st.session_state.player = "All"
            st.session_state.year = "All"
            selected_team = 'All'
            selected_player = 'All'
            selected_year = 'All'
            selectedRosters = Rosters
    st.button('Reset Filters', on_click=reset_filters)
    
    team_list = list(Rosters.Owner.unique())
    # Remove nan values
    team_list = [x for x in team_list if x == x]
    print(team_list)
    team_list.sort()
    team_list.insert(0, 'All')
    selected_team = st.selectbox('Team', team_list, index=0, key='team')

    if selected_team == 'All':
        selectedRosters = Rosters
    else:
        selectedRosters = Rosters[Rosters.Owner == selected_team]

    year_list = list(selectedRosters.Year.unique())[::-1]
    year_list.sort()
    year_list.insert(0, 'All')
    selected_year = st.selectbox('Year', year_list, index=0, key='year')
    if selected_year == 'All':
        selectedRosters = selectedRosters
    else:
        selectedRosters = selectedRosters[selectedRosters.Year == selected_year] 

    player_list = list(selectedRosters.Player.unique())
    player_list.sort()
    player_list.insert(0, 'All')
    selected_player = st.selectbox('Player', player_list, index=0, key='player')
    if selected_player == 'All':
        selectedRosters = selectedRosters
    else:
        selectedRosters = selectedRosters[selectedRosters.Player == selected_player]   

# If player/year is selected, pull Savant data
savant = False
hitter = False
pitcher = False
if (selected_player != 'All') and (selected_year != 'All'):
    savant = True

    # Hitter data
    hitter_ranks = pyb.statcast_batter_percentile_ranks(selected_year)
    hitter_ranks['player_name'] = hitter_ranks['player_name'].apply(lambda x: unidecode.unidecode(x) if isinstance(x, str) else x)
    hitter_ranks[['last_name', 'first_name']] = hitter_ranks['player_name'].str.split(',', expand=True).apply(lambda x: x.str.strip())
    hitter_ranks['Name'] = hitter_ranks['first_name'] + " " + hitter_ranks['last_name']
    hitter_ranks = hitter_ranks[hitter_ranks['Name'] == selected_player]
    if not hitter_ranks.empty:
        hitter = True
        f_name = hitter_ranks['first_name'].iloc[0]
        l_name = hitter_ranks['last_name'].iloc[0]
        id = hitter_ranks['player_id'].iloc[0]
        f_name_url = f_name.replace(' ', '-')
        l_name_url = l_name.replace(' ', '-')
        id_url = hitter_ranks['player_id'].iloc[0].astype(str)
    hitter_ranks = hitter_ranks[['Name', 'xwoba', 'xba', 'xslg', 'exit_velocity', 'brl_percent', 'hard_hit_percent', 'bat_speed', 'chase_percent', 'whiff_percent', 'k_percent', 'bb_percent']]
    hitter_ranks.columns = ['Name', 'xwOBA', 'xBA', 'xSLG', 'Exit Velocity', 'Barrel %', 'Hard-Hit %', 'Bat Speed', 'Chase %', 'Whiff %', 'K %', 'BB %']
    hitter_ranks = hitter_ranks.melt(id_vars=['Name'], var_name='stat', value_name='value')

    # Pitcher data
    pitcher_ranks = pyb.statcast_pitcher_percentile_ranks(selected_year)
    pitcher_ranks['player_name'] = pitcher_ranks['player_name'].apply(lambda x: unidecode.unidecode(x) if isinstance(x, str) else x)
    pitcher_ranks[['last_name', 'first_name']] = pitcher_ranks['player_name'].str.split(',', expand=True).apply(lambda x: x.str.strip())
    pitcher_ranks['Name'] = pitcher_ranks['first_name'] + " " + pitcher_ranks['last_name']
    pitcher_ranks = pitcher_ranks[pitcher_ranks['Name'] == selected_player]
    if not pitcher_ranks.empty:
        pitcher = True
        f_name = pitcher_ranks['first_name'].iloc[0]
        l_name = pitcher_ranks['last_name'].iloc[0]
        f_name_url = f_name.replace(' ', '-')
        l_name_url = l_name.replace(' ', '-')
        id = pitcher_ranks['player_id'].iloc[0]
        id_url = pitcher_ranks['player_id'].iloc[0].astype(str)
    pitcher_ranks = pitcher_ranks[['Name', 'xera', 'xba', 'fb_velocity', 'exit_velocity', 'chase_percent', 'whiff_percent', 'k_percent', 'bb_percent', 'brl_percent', 'hard_hit_percent']]
    pitcher_ranks.columns = ['Name', 'xERA', 'xBA', 'Fastball Velocity', 'Exit Velocity', 'Chase %', 'Whiff %', 'K %', 'BB %', 'Barrel %', 'Hard-Hit %']
    pitcher_ranks = pitcher_ranks.melt(id_vars=['Name'], var_name='stat', value_name='value')

# If player/year is selected, pull Bref data
if savant:
    if hitter:
        batting_stats = pyb.batting_stats_bref(season = selected_year)  
        batting_stats = batting_stats[batting_stats.mlbID == id]
        batting_stats = batting_stats[['Name', 'Age', 'Tm', 'G', 'PA', 'AB', 'R', 'H', 'HR', 'RBI', 'SO', 'SB', 'BA', 'OBP', 'OPS']]

    if pitcher:
        pitching_stats = pyb.pitching_stats_bref(season = selected_year)
        pitching_stats = pitching_stats[pitching_stats.mlbID == id_url]
        pitching_stats = pitching_stats[['Name', 'Age', 'Tm', 'G', 'GS', 'W', 'L', 'SV', 'IP', 'ER', 'BB', 'ERA', 'WHIP', 'SO9']]

# Used for URLs
if (hitter) or (pitcher):
    lookup = pyb.playerid_reverse_lookup([id])
    bref_id = lookup.key_bbref.values[0]
    fg_id = lookup.key_fangraphs.values[0]
    bref_abrv = l_name[0].lower()

col = st.columns((1, 2), gap='small')
with col[0]:
    st.markdown('<h3 style="text-align: left;">Rosters</h3>', unsafe_allow_html=True)
    st.dataframe(selectedRosters, hide_index=True, width=900)
    if savant:
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
            st.write(f"Data sourced from [Baseball Savant](https://baseballsavant.mlb.com/savant-player/{f_name_url}-{l_name_url}-{id_url})")
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
            st.write(f"Data sourced from [Baseball Savant](https://baseballsavant.mlb.com/savant-player/{f_name_url}-{l_name_url}-{id_url})")
        if (not hitter) and (not pitcher):
            st.write(f"Player not found in database. Please check the [Baseball Savant](https://baseballsavant.mlb.com) page directly.")

if savant:
    with col[1]:
        st.markdown('<h3 style="text-align: center;">Season Statistics</h3>', unsafe_allow_html=True)
        if hitter:
            st.dataframe(batting_stats, hide_index=True, width=1000)
        if pitcher:
            st.dataframe(pitching_stats, hide_index=True, width=1000)
        st.write(f"Data sourced from [Baseball Reference](https://www.baseball-reference.com/players/{bref_abrv}/{bref_id}.shtml)")
        st.write(f"More data can be found on [Fangraphs](https://www.fangraphs.com/players/{f_name_url}-{l_name_url}/{fg_id}/stats)")
else: 
    with col[1]:
        st.markdown('<h3 style="text-align: center;">Select a player and year combination to see statistics!</h3>', unsafe_allow_html=True)


