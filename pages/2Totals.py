# Fantasy DB - Totals

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Fantasy Dashboard",
    layout="wide",
    initial_sidebar_state="auto")

# Import data - needs manually uploaded and committed to GitHub
WeeklyData_full = pd.read_excel('data/FantasyData.xlsx', sheet_name='WeeklyData')
WeeklyData_full = WeeklyData_full[WeeklyData_full['Week'] != WeeklyData_full['Week'].max()]

with st.sidebar:  
    def reset_filters():
            st.session_state.type = "Head to Head"
            st.session_state.team = 'All'
            selected_type = 'Head to Head'
            selected_team = 'All'
    st.button('Reset Filters', on_click=reset_filters)
    selected_type = st.selectbox('Rank Type', ['Head to Head', 'Overall'], index=0, key='type')
    team_list = list(WeeklyData_full.Team.unique())[::-1]
    # Remove nan values
    team_list = [x for x in team_list if x == x]
    team_list.sort()
    team_list.insert(0, 'All')
    selected_team = st.selectbox('Team', team_list, index=0, key='team')

# Creating H2H win totals dataframe
columns = ['R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD']
Wins = pd.DataFrame()
for col in columns:
    Wins[col] = WeeklyData_full.groupby('Team')[col].apply(lambda x: (x == 'WIN').sum())
    Wins[col] = Wins[col] + (WeeklyData_full.groupby('Team')[col].apply(lambda x: (x == 'TIE').sum())*.5)

Wins.reset_index(inplace=True)
Wins['Wins'] = Wins.sum(axis=1)
Wins.sort_values(by='Wins', inplace=True, ascending=False)

# Creating H2H ranks dataframe
HH_ranks = Wins.copy()
columns = ['Wins', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD']
for col in columns:
    HH_ranks[col] = HH_ranks[col].rank(method='min', ascending=False)

# Creating roto totals dataframe
Totals = pd.DataFrame()
total_columns = ['R', 'HR', 'RBI', 'SB', 'K', 'W', 'SVHD']
for col in total_columns:
    Totals[col] = WeeklyData_full.groupby('Team').apply(lambda x: x[col+'_val'].sum())
Totals['OBP'] = WeeklyData_full.groupby('Team').apply(lambda x: x['OBP_val'].mean())
Totals['ERA'] = WeeklyData_full.groupby('Team').apply(lambda x: x['ERA_val'].mean())
Totals['WHIP'] = WeeklyData_full.groupby('Team').apply(lambda x: x['WHIP_val'].mean())
Totals['sum'] = Totals.sum(axis=1)
Totals['Rank'] = Totals['sum'].rank(method='min', ascending=False)
Totals.sort_values(by='Rank', inplace=True)
Totals.reset_index(inplace=True)

# Creating roto ranks dataframe
roto_ranks = Totals.copy()
columns = ['R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'SVHD']
for col in columns:
    roto_ranks[col] = roto_ranks[col].rank(method='min', ascending=False)

roto_ranks['ERA'] = roto_ranks['ERA'].rank(method='min', ascending=True)
roto_ranks['WHIP'] = roto_ranks['WHIP'].rank(method='min', ascending=True)

# Highlight highest point values in gold
def highlight_top3(s):
    top3 = s.nlargest(3)
    return ['color: gold' if v in top3.values else '' for v in s]
def highlight_bot3(s):
    top3 = s.nsmallest(3)
    return ['color: gold' if v in top3.values else '' for v in s]

# Apply gold formatting
if selected_team == 'All':
    Wins_style = Wins.style.apply(highlight_top3, subset=['R'], axis=0).apply(highlight_top3, subset=['HR'], axis=0)\
        .apply(highlight_top3, subset=['RBI'], axis=0).apply(highlight_top3, subset=['SB'], axis=0)\
        .apply(highlight_top3, subset=['OBP'], axis=0).apply(highlight_top3, subset=['K'], axis=0)\
        .apply(highlight_top3, subset=['W'], axis=0).apply(highlight_top3, subset=['ERA'], axis=0)\
        .apply(highlight_top3, subset=['WHIP'], axis=0).apply(highlight_top3, subset=['SVHD'], axis=0)
    Wins_style.format({col: "{:.1f}" for col in Wins.select_dtypes('number').columns})

    HH_ranks_style = HH_ranks.style.apply(highlight_bot3, subset=['R'], axis=0).apply(highlight_bot3, subset=['HR'], axis=0)\
        .apply(highlight_bot3, subset=['RBI'], axis=0).apply(highlight_bot3, subset=['SB'], axis=0)\
        .apply(highlight_bot3, subset=['OBP'], axis=0).apply(highlight_bot3, subset=['K'], axis=0)\
        .apply(highlight_bot3, subset=['W'], axis=0).apply(highlight_bot3, subset=['ERA'], axis=0)\
        .apply(highlight_bot3, subset=['WHIP'], axis=0).apply(highlight_bot3, subset=['SVHD'], axis=0)
    HH_ranks_style.format({col: "{:.0f}" for col in Wins.select_dtypes('number').columns})

    Totals_style = Totals.style.apply(highlight_top3, subset=['R'], axis=0).apply(highlight_top3, subset=['HR'], axis=0)\
        .apply(highlight_top3, subset=['RBI'], axis=0).apply(highlight_top3, subset=['SB'], axis=0)\
        .apply(highlight_top3, subset=['OBP'], axis=0).apply(highlight_top3, subset=['K'], axis=0)\
        .apply(highlight_top3, subset=['W'], axis=0).apply(highlight_bot3, subset=['ERA'], axis=0)\
        .apply(highlight_bot3, subset=['WHIP'], axis=0).apply(highlight_top3, subset=['SVHD'], axis=0)
    Totals_style.format({col: "{:.3f}" for col in ['OBP', 'ERA', 'WHIP']})
    Totals_style.format({col: "{:.0f}" for col in ['Rank']})

    roto_style = roto_ranks.style.apply(highlight_bot3, subset=['R'], axis=0).apply(highlight_bot3, subset=['HR'], axis=0)\
        .apply(highlight_bot3, subset=['RBI'], axis=0).apply(highlight_bot3, subset=['SB'], axis=0)\
        .apply(highlight_bot3, subset=['OBP'], axis=0).apply(highlight_bot3, subset=['K'], axis=0)\
        .apply(highlight_bot3, subset=['W'], axis=0).apply(highlight_bot3, subset=['ERA'], axis=0)\
        .apply(highlight_bot3, subset=['WHIP'], axis=0).apply(highlight_bot3, subset=['SVHD'], axis=0)
    roto_style.format({col: "{:.0f}" for col in roto_ranks.select_dtypes('number').columns})

if selected_team != 'All':
    Wins_style = Wins[Wins['Team'] == selected_team]
    HH_ranks_style = HH_ranks[HH_ranks['Team'] == selected_team]
    Totals_style = Totals[Totals['Team'] == selected_team]
    roto_style = roto_ranks[roto_ranks['Team'] == selected_team]

if selected_type == 'Head to Head':
    st.markdown('<h3 style="text-align: center;">H2H Win Totals</h3>', unsafe_allow_html=True)
    st.dataframe(Wins_style, width=2000, height=457, hide_index=True, column_order=['Team', 'Wins', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD'])
    st.write('')
    st.markdown('<h3 style="text-align: center;">H2H Ranks</h3>', unsafe_allow_html=True)
    st.dataframe(HH_ranks_style, width=2000, height=457, hide_index=True, column_order=['Team', 'Wins', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD'])
if selected_type == 'Overall':
    st.markdown('<h3 style="text-align: center;">Overall Totals</h3>', unsafe_allow_html=True)
    st.dataframe(Totals_style, width=1000, height=457, hide_index=True, column_order=['Team', 'Rank', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD'])
    st.write('')
    st.markdown('<h3 style="text-align: center;">Overall Ranks</h3>', unsafe_allow_html=True)
    st.dataframe(roto_style, width=1000, height=457, hide_index=True, column_order=['Team', 'Rank', 'Wins', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD'])
    


