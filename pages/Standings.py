# Fantasy DB - Standings

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Fantasy Dashboard",
    layout="wide",
    initial_sidebar_state="auto")

# Import data - needs manually uploaded and committed to GitHub
WeeklyData = pd.read_excel('data/FantasyData.xlsx', sheet_name='WeeklyData')

# Prepare Standings Dashboard
def count_wins(series):
    return (series == 'WIN').sum()

# Group by 'Team' and apply the function to each group
# WeeklyData = WeeklyData[['Team', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD']]
# WeeklyData = WeeklyData.groupby('Team').apply(count_wins)
# Prepare Scoreboard Dashboard
WeeklyData['Record'] = WeeklyData.apply(lambda row: (row == 'WIN').sum(), axis=1).astype(str) + '-' + (WeeklyData.apply(lambda row: (row == 'LOSS').sum(), axis=1)).astype(str) + '-' + (WeeklyData.apply(lambda row: (row == 'TIE').sum(), axis=1)).astype(str)
WeeklyData['Points'] = WeeklyData.apply(lambda row: (row == 'WIN').sum(), axis=1) + (WeeklyData.apply(lambda row: (row == 'TIE').sum(), axis=1) * 0.5)
WeeklyData = WeeklyData[['Team', 'Record', 'R_val', 'HR_val', 'RBI_val', 'SB_val', 'OBP_val', 'K_val', 'W_val', 'ERA_val', 'WHIP_val', 'SVHD_val', 'Opponent', 'Points', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD']]
WeeklyData.columns = ['Team', 'Record', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD', 'Opponent', 'Points', 'Ro', 'HRo', 'RBIo', 'SBo', 'OBPo', 'Ko', 'Wo', 'ERAo', 'WHIPo', 'SVHDo']
WeeklyData.sort_values(by='Points', ascending=False, inplace=True)
WeeklyData.reset_index(drop=True, inplace=True)
WeeklyData.index = WeeklyData.index + 1
WeeklyData.index.name = 'Rank'

st.markdown('<h3 style="text-align: center;">Weekly Winners</h3>', unsafe_allow_html=True)
container = st.container()
with container:
    st.dataframe(WeeklyData)


