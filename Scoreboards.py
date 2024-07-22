# Fantasy DB - Scoreboards - Homepage

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Fantasy Dashboard",
    layout="wide",
    initial_sidebar_state="auto")

# Import data - needs manually uploaded and committed to GitHub
WeeklyData = pd.read_excel('data/FantasyData.xlsx', sheet_name='WeeklyData')

# Filters
with st.sidebar:  
    team_list = list(WeeklyData.Team.unique())[::-1]
    team_list.append('All')
    team_list.sort()
    selected_team = st.selectbox('Team', team_list, index=0)
    if selected_team == 'All':
        WeeklyData = WeeklyData
    else:
        WeeklyData = WeeklyData[WeeklyData.Team == selected_team]

    week_list = list(WeeklyData.Week.unique())[::-1]
    week_list.append(0)
    week_list.sort()
    selected_week = st.selectbox('Week (select 0 for all previous)', week_list, index=0)

# Prepare Scoreboard Dashboard
max_week = WeeklyData['Week'].max()
CurrentWeeklyData = WeeklyData[WeeklyData['Week'] == max_week]
CurrentWeeklyData = CurrentWeeklyData.drop(['Week'], axis=1)
CurrentWeeklyData['Record'] = CurrentWeeklyData.apply(lambda row: (row == 'WIN').sum(), axis=1).astype(str) + '-' + (CurrentWeeklyData.apply(lambda row: (row == 'LOSS').sum(), axis=1)).astype(str) + '-' + (CurrentWeeklyData.apply(lambda row: (row == 'TIE').sum(), axis=1)).astype(str)
CurrentWeeklyData['Points'] = CurrentWeeklyData.apply(lambda row: (row == 'WIN').sum(), axis=1) + (CurrentWeeklyData.apply(lambda row: (row == 'TIE').sum(), axis=1) * 0.5)
CurrentWeeklyData['OBP_val'] = CurrentWeeklyData['OBP_val'].map('{:.3f}'.format)
CurrentWeeklyData['ERA_val'] = CurrentWeeklyData['ERA_val'].map('{:.2f}'.format)
CurrentWeeklyData['WHIP_val'] = CurrentWeeklyData['WHIP_val'].map('{:.2f}'.format)
CurrentWeeklyData = CurrentWeeklyData[['Team', 'Record', 'R_val', 'HR_val', 'RBI_val', 'SB_val', 'OBP_val', 'K_val', 'W_val', 'ERA_val', 'WHIP_val', 'SVHD_val', 'Opponent', 'Points', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD']]
CurrentWeeklyData.columns = ['Team', 'Record', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD', 'Opponent', 'Points', 'Ro', 'HRo', 'RBIo', 'SBo', 'OBPo', 'Ko', 'Wo', 'ERAo', 'WHIPo', 'SVHDo']
CurrentWeeklyData.sort_values(by='Points', ascending=False, inplace=True)
CurrentWeeklyData.reset_index(drop=True, inplace=True)
CurrentWeeklyData.index = CurrentWeeklyData.index + 1
CurrentWeeklyData.index.name = 'Rank'

if selected_week == 0:
    PreviousWeeklyData = WeeklyData[WeeklyData['Week'] != max_week]
else:
    PreviousWeeklyData = WeeklyData[WeeklyData['Week'] == selected_week]
PreviousWeeklyData['Record'] = PreviousWeeklyData.apply(lambda row: (row == 'WIN').sum(), axis=1).astype(str) + '-' + (PreviousWeeklyData.apply(lambda row: (row == 'LOSS').sum(), axis=1)).astype(str) + '-' + (PreviousWeeklyData.apply(lambda row: (row == 'TIE').sum(), axis=1)).astype(str)
PreviousWeeklyData['Points'] = PreviousWeeklyData.apply(lambda row: (row == 'WIN').sum(), axis=1) + (PreviousWeeklyData.apply(lambda row: (row == 'TIE').sum(), axis=1) * 0.5)
PreviousWeeklyData['OBP_val'] = PreviousWeeklyData['OBP_val'].map('{:.3f}'.format)
PreviousWeeklyData['ERA_val'] = PreviousWeeklyData['ERA_val'].map('{:.2f}'.format)
PreviousWeeklyData['WHIP_val'] = PreviousWeeklyData['WHIP_val'].map('{:.2f}'.format)
PreviousWeeklyData = PreviousWeeklyData[['Week', 'Team', 'Record', 'R_val', 'HR_val', 'RBI_val', 'SB_val', 'OBP_val', 'K_val', 'W_val', 'ERA_val', 'WHIP_val', 'SVHD_val', 'Opponent', 'Points', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD']]
PreviousWeeklyData.columns = ['Week', 'Team', 'Record', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD', 'Opponent', 'Points', 'Ro', 'HRo', 'RBIo', 'SBo', 'OBPo', 'Ko', 'Wo', 'ERAo', 'WHIPo', 'SVHDo']
PreviousWeeklyData = PreviousWeeklyData.sort_values(by=['Team', 'Week'])
PreviousWeeklyData.reset_index(drop=True, inplace=True)
PreviousWeeklyData.index = PreviousWeeklyData.index + 1
PreviousWeeklyData.index.name = 'Order'

# Conditional formatting based on results
def highlight_val(data, col, val_col):
    color = '#17e310' if data[col] == 'WIN' else '#ed1c1c' if data[col] == 'LOSS' else ''
    return ['background-color: %s' % color if column == val_col else '' for column in data.index]
def highlight_records(data, col, val_col):
    color = '#17e310' if data[col] > 5 else '#ed1c1c' if data[col] < 5 else ''
    return ['color: %s' % color if column == val_col else '' for column in data.index]
def highlight_max(s):
    is_max = s == s.max()
    return ['color: gold' if v else '' for v in is_max]
def highlight_min(s):
    is_min = s == s.min()
    return ['color: gold' if v else '' for v in is_min]

# Applying conditional formats
if selected_team == 'All':
    style_df = CurrentWeeklyData.style.apply(highlight_val, col='Ro', val_col='R', axis=1).apply(highlight_val, col='HRo', val_col='HR', axis=1)\
    .apply(highlight_val, col='RBIo', val_col='RBI', axis=1).apply(highlight_val, col='SBo', val_col='SB', axis=1)\
    .apply(highlight_val, col='OBPo', val_col='OBP', axis=1).apply(highlight_val, col='Ko', val_col='K', axis=1)\
    .apply(highlight_val, col='Wo', val_col='W', axis=1).apply(highlight_val, col='ERAo', val_col='ERA', axis=1)\
    .apply(highlight_val, col='WHIPo', val_col='WHIP', axis=1).apply(highlight_val, col='SVHDo', val_col='SVHD', axis=1)\
    .apply(highlight_records, col='Points', val_col='Record', axis=1)\
    .apply(highlight_max, subset=['R'], axis=0).apply(highlight_max, subset=['HR'], axis=0)\
    .apply(highlight_max, subset=['RBI'], axis=0).apply(highlight_max, subset=['SB'], axis=0)\
    .apply(highlight_max, subset=['OBP'], axis=0).apply(highlight_max, subset=['K'], axis=0)\
    .apply(highlight_max, subset=['W'], axis=0).apply(highlight_min, subset=['ERA'], axis=0)\
    .apply(highlight_min, subset=['WHIP'], axis=0).apply(highlight_max, subset=['SVHD'], axis=0)
else:
    style_df = CurrentWeeklyData.style.apply(highlight_val, col='Ro', val_col='R', axis=1).apply(highlight_val, col='HRo', val_col='HR', axis=1)\
    .apply(highlight_val, col='RBIo', val_col='RBI', axis=1).apply(highlight_val, col='SBo', val_col='SB', axis=1)\
    .apply(highlight_val, col='OBPo', val_col='OBP', axis=1).apply(highlight_val, col='Ko', val_col='K', axis=1)\
    .apply(highlight_val, col='Wo', val_col='W', axis=1).apply(highlight_val, col='ERAo', val_col='ERA', axis=1)\
    .apply(highlight_val, col='WHIPo', val_col='WHIP', axis=1).apply(highlight_val, col='SVHDo', val_col='SVHD', axis=1)\
    .apply(highlight_records, col='Points', val_col='Record', axis=1)


if selected_team == 'All' or selected_week == 0:
    prev_style_df = PreviousWeeklyData.style.apply(highlight_val, col='Ro', val_col='R', axis=1).apply(highlight_val, col='HRo', val_col='HR', axis=1)\
    .apply(highlight_val, col='RBIo', val_col='RBI', axis=1).apply(highlight_val, col='SBo', val_col='SB', axis=1)\
    .apply(highlight_val, col='OBPo', val_col='OBP', axis=1).apply(highlight_val, col='Ko', val_col='K', axis=1)\
    .apply(highlight_val, col='Wo', val_col='W', axis=1).apply(highlight_val, col='ERAo', val_col='ERA', axis=1)\
    .apply(highlight_val, col='WHIPo', val_col='WHIP', axis=1).apply(highlight_val, col='SVHDo', val_col='SVHD', axis=1)\
    .apply(highlight_records, col='Points', val_col='Record', axis=1)\
    .apply(highlight_max, subset=['R'], axis=0).apply(highlight_max, subset=['HR'], axis=0)\
    .apply(highlight_max, subset=['RBI'], axis=0).apply(highlight_max, subset=['SB'], axis=0)\
    .apply(highlight_max, subset=['OBP'], axis=0).apply(highlight_max, subset=['K'], axis=0)\
    .apply(highlight_max, subset=['W'], axis=0).apply(highlight_min, subset=['ERA'], axis=0)\
    .apply(highlight_min, subset=['WHIP'], axis=0).apply(highlight_max, subset=['SVHD'], axis=0)
else:
    prev_style_df = PreviousWeeklyData.style.apply(highlight_val, col='Ro', val_col='R', axis=1).apply(highlight_val, col='HRo', val_col='HR', axis=1)\
    .apply(highlight_val, col='RBIo', val_col='RBI', axis=1).apply(highlight_val, col='SBo', val_col='SB', axis=1)\
    .apply(highlight_val, col='OBPo', val_col='OBP', axis=1).apply(highlight_val, col='Ko', val_col='K', axis=1)\
    .apply(highlight_val, col='Wo', val_col='W', axis=1).apply(highlight_val, col='ERAo', val_col='ERA', axis=1)\
    .apply(highlight_val, col='WHIPo', val_col='WHIP', axis=1).apply(highlight_val, col='SVHDo', val_col='SVHD', axis=1)\
    .apply(highlight_records, col='Points', val_col='Record', axis=1)

# Creating visuals
container = st.container()
with container:
    st.markdown('<h3 style="text-align: center;">Current Scoreboard</h3>', unsafe_allow_html=True)
    st.dataframe(style_df, height=457, width=1500)
    st.write("")
    st.write("")
    st.divider()
    st.write("")
    st.write("")
    st.markdown('<h3 style="text-align: center;">Season Scoreboard</h3>', unsafe_allow_html=True)
    st.dataframe(prev_style_df, height=457, width=1500)


