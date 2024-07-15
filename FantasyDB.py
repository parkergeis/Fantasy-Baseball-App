# Fantasy DB

import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.set_page_config(
    page_title="Fantasy Dashboard",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


# Import data - needs manually uploaded and committed to GitHub
WeeklyData = pd.read_excel('data/FantasyData.xlsx', sheet_name='WeeklyData')
Standings = pd.read_excel('data/FantasyData.xlsx', sheet_name='PreviousStandings')
Rosters = pd.read_excel('data/FantasyData.xlsx', sheet_name='Rosters')

WeeklyData['Points'] = WeeklyData.apply(lambda row: (row == 'WIN').sum(), axis=1) + (WeeklyData.apply(lambda row: (row == 'TIE').sum(), axis=1) * 0.5)
WeeklyData['Points'] = WeeklyData['Points'].map('{:.1f}'.format)
WeeklyData['OBP_val'] = WeeklyData['OBP_val'].map('{:.3f}'.format)
WeeklyData['ERA_val'] = WeeklyData['ERA_val'].map('{:.2f}'.format)
WeeklyData['WHIP_val'] = WeeklyData['WHIP_val'].map('{:.2f}'.format)
WeeklyData = WeeklyData[['Week', 'Team', 'R_val', 'HR_val', 'RBI_val', 'SB_val', 'OBP_val', 'K_val', 'W_val', 'ERA_val', 'WHIP_val', 'SVHD_val', 'Opponent', 'Points', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD']]

# Prepare Current Scoreboard Dashboard
max_week = WeeklyData['Week'].max()
CurrentWeeklyData = WeeklyData[WeeklyData['Week'] == max_week]
CurrentWeeklyData = CurrentWeeklyData.drop(['Week'], axis=1)
CurrentWeeklyData.sort_values(by='Points', ascending=False, inplace=True)
CurrentWeeklyData.reset_index(drop=True, inplace=True)
CurrentWeeklyData.index = CurrentWeeklyData.index + 1
CurrentWeeklyData.index.name = 'Rank'


# Conditional formatting based on results
def highlight_val(data, col, val_col):
    color = 'green' if data[col] == 'WIN' else 'red' if data[col] == 'LOSS' else ''
    return ['background-color: %s' % color if column == val_col else '' for column in data.index]
def highlight_max(s):
    is_max = s == s.max()
    return ['color: gold' if v else '' for v in is_max]
def highlight_min(s):
    is_min = s == s.min()
    return ['color: gold' if v else '' for v in is_min]

# Usage
style_df = CurrentWeeklyData.style.apply(highlight_val, col='R', val_col='R_val', axis=1).apply(highlight_val, col='HR', val_col='HR_val', axis=1)\
.apply(highlight_val, col='RBI', val_col='RBI_val', axis=1).apply(highlight_val, col='SB', val_col='SB_val', axis=1)\
.apply(highlight_val, col='OBP', val_col='OBP_val', axis=1).apply(highlight_val, col='K', val_col='K_val', axis=1)\
.apply(highlight_val, col='W', val_col='W_val', axis=1).apply(highlight_val, col='ERA', val_col='ERA_val', axis=1)\
.apply(highlight_val, col='WHIP', val_col='WHIP_val', axis=1).apply(highlight_val, col='SVHD', val_col='SVHD_val', axis=1)\
.apply(highlight_max, subset=['R_val'], axis=0).apply(highlight_max, subset=['HR_val'], axis=0)\
.apply(highlight_max, subset=['RBI_val'], axis=0).apply(highlight_max, subset=['SB_val'], axis=0)\
.apply(highlight_max, subset=['OBP_val'], axis=0).apply(highlight_max, subset=['K_val'], axis=0)\
.apply(highlight_max, subset=['W_val'], axis=0).apply(highlight_min, subset=['ERA_val'], axis=0)\
.apply(highlight_min, subset=['WHIP_val'], axis=0).apply(highlight_max, subset=['SVHD_val'], axis=0)

st.dataframe(style_df, width=1150, height=457)



