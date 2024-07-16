# Fantasy DB - Current Week - Homepage

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Fantasy Dashboard",
    layout="wide")

# Import data - needs manually uploaded and committed to GitHub
WeeklyData = pd.read_excel('data/FantasyData.xlsx', sheet_name='WeeklyData')

# Prepare Current Scoreboard Dashboard
max_week = WeeklyData['Week'].max()
CurrentWeeklyData = WeeklyData[WeeklyData['Week'] == max_week]
CurrentWeeklyData = CurrentWeeklyData.drop(['Week'], axis=1)
CurrentWeeklyData['Points'] = CurrentWeeklyData.apply(lambda row: (row == 'WIN').sum(), axis=1) + (CurrentWeeklyData.apply(lambda row: (row == 'TIE').sum(), axis=1) * 0.5)
CurrentWeeklyData['Points'] = CurrentWeeklyData['Points'].map('{:.1f}'.format)
CurrentWeeklyData['OBP_val'] = CurrentWeeklyData['OBP_val'].map('{:.3f}'.format)
CurrentWeeklyData['ERA_val'] = CurrentWeeklyData['ERA_val'].map('{:.2f}'.format)
CurrentWeeklyData['WHIP_val'] = CurrentWeeklyData['WHIP_val'].map('{:.2f}'.format)
CurrentWeeklyData = CurrentWeeklyData[['Week', 'Team', 'R_val', 'HR_val', 'RBI_val', 'SB_val', 'OBP_val', 'K_val', 'W_val', 'ERA_val', 'WHIP_val', 'SVHD_val', 'Opponent', 'Points', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD']]
CurrentWeeklyData.columns = ['Week', 'Team', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD', 'Opponent', 'Points', 'Ro', 'HRo', 'RBIo', 'SBo', 'OBPo', 'Ko', 'Wo', 'ERAo', 'WHIPo', 'SVHDo']
CurrentWeeklyData.sort_values(by='Points', ascending=False, inplace=True)
CurrentWeeklyData.reset_index(drop=True, inplace=True)
CurrentWeeklyData.index = CurrentWeeklyData.index + 1
CurrentWeeklyData.index.name = 'Rank'

# Conditional formatting based on results
def highlight_val(data, col, val_col):
    color = '#17e310' if data[col] == 'WIN' else '#ed1c1c' if data[col] == 'LOSS' else ''
    return ['background-color: %s' % color if column == val_col else '' for column in data.index]
def highlight_max(s):
    is_max = s == s.max()
    return ['color: gold' if v else '' for v in is_max]
def highlight_min(s):
    is_min = s == s.min()
    return ['color: gold' if v else '' for v in is_min]

# Applying conditional formats
style_df = CurrentWeeklyData.style.apply(highlight_val, col='Ro', val_col='R', axis=1).apply(highlight_val, col='HRo', val_col='HR', axis=1)\
.apply(highlight_val, col='RBIo', val_col='RBI', axis=1).apply(highlight_val, col='SBo', val_col='SB', axis=1)\
.apply(highlight_val, col='OBPo', val_col='OBP', axis=1).apply(highlight_val, col='Ko', val_col='K', axis=1)\
.apply(highlight_val, col='Wo', val_col='W', axis=1).apply(highlight_val, col='ERAo', val_col='ERA', axis=1)\
.apply(highlight_val, col='WHIPo', val_col='WHIP', axis=1).apply(highlight_val, col='SVHDo', val_col='SVHD', axis=1)\
.apply(highlight_max, subset=['R'], axis=0).apply(highlight_max, subset=['HR'], axis=0)\
.apply(highlight_max, subset=['RBI'], axis=0).apply(highlight_max, subset=['SB'], axis=0)\
.apply(highlight_max, subset=['OBP'], axis=0).apply(highlight_max, subset=['K'], axis=0)\
.apply(highlight_max, subset=['W'], axis=0).apply(highlight_min, subset=['ERA'], axis=0)\
.apply(highlight_min, subset=['WHIP'], axis=0).apply(highlight_max, subset=['SVHD'], axis=0).hide_index()

st.markdown('<h3 style="text-align: center;">Current Scoreboard</h3>', unsafe_allow_html=True)
container = st.container()
with container:
    st.dataframe(style_df, height=457, width=1500)  # Specify height here
        
# st.write("") # Use to add gaps


