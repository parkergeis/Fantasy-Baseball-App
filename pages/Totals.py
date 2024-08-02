# Fantasy DB - Totals

# Apply cond. formatting
# Add button/slicer to choose H2H or roto?
# Add filter for team(s)?

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
            st.session_state.team = '1All'
            selected_type = 'Head to Head'
            selected_team = '1All'
    st.button('Reset Filters', on_click=reset_filters)
    selected_type = st.selectbox('Rank Type', ['Head to Head', 'Overall'], index=0, key='type')
    team_list = list(WeeklyData_full.Team.unique())[::-1]
    team_list.append('1All')
    team_list.sort()
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
Totals.reset_index(inplace=True)

# Creating roto ranks dataframe
roto_ranks = Totals.copy()
columns = ['R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD']
for col in columns:
    roto_ranks[col] = roto_ranks[col].rank(method='min', ascending=False)

# Highlight highest point values in gold
def highlight_max(s):
    is_max = s == s.max()
    return ['color: gold' if v else '' for v in is_max]

# style_df = Wins.style.apply(highlight_max, subset=['R'], axis=0).apply(highlight_max, subset=['HR'], axis=0)\
#     .apply(highlight_max, subset=['RBI'], axis=0).apply(highlight_max, subset=['SB'], axis=0)\
#     .apply(highlight_max, subset=['OBP'], axis=0).apply(highlight_max, subset=['K'], axis=0)\
#     .apply(highlight_max, subset=['W'], axis=0).apply(highlight_max, subset=['ERA'], axis=0)\
#     .apply(highlight_max, subset=['WHIP'], axis=0).apply(highlight_max, subset=['SVHD'], axis=0)

if selected_team != '1All':
    Wins = Wins[Wins['Team'] == selected_team]
    HH_ranks = HH_ranks[HH_ranks['Team'] == selected_team]
    Totals = Totals[Totals['Team'] == selected_team]
    roto_ranks = roto_ranks[roto_ranks['Team'] == selected_team]

col = st.columns((1, 10, 1), gap='medium')
with col[1]:
    if selected_type == 'Head to Head':
        st.markdown('<h3 style="text-align: center;">H2H Win Totals</h3>', unsafe_allow_html=True)
        st.dataframe(Wins, width=2000, height=457, hide_index=True, column_order=['Team', 'Wins', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD'])
        st.write('')
        st.markdown('<h3 style="text-align: center;">H2H Ranks</h3>', unsafe_allow_html=True)
        st.dataframe(HH_ranks, width=1000, height=457, hide_index=True, column_order=['Team', 'Wins', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD'])
    if selected_type == 'Overall':
        st.markdown('<h3 style="text-align: center;">Overall Totals</h3>', unsafe_allow_html=True)
        st.dataframe(Totals, width=1000, height=457, hide_index=True, column_order=['Team', 'Wins', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD'])
        st.write('')
        st.markdown('<h3 style="text-align: center;">Overall Ranks</h3>', unsafe_allow_html=True)
        st.dataframe(roto_ranks, width=1000, height=457, hide_index=True, column_order=['Team', 'Rank', 'Wins', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD'])
    


