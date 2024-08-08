# Fantasy DB - Scoreboards - Homepage

# import espn_data_import
import streamlit as st
import pandas as pd
import numpy as np
import gspread

st.set_page_config(
    page_title="Fantasy Dashboard",
    layout="wide",
    initial_sidebar_state="auto")

# Select data from import
gc = gspread.service_account(filename='/Users/parkergeis/.config/gspread/seismic-bucksaw-427616-e6-7082af692c88.json')

sh = gc.open("FantasyData")
worksheet = sh.sheet1
data = worksheet.get_all_records()
WeeklyData_full = pd.DataFrame(data)
#WeeklyData_full = pd.read_excel('data/FantasyData.xlsx', sheet_name='WeeklyData')
WeeklyData_full['Record'] = WeeklyData_full.apply(lambda row: (row == 'WIN').sum(), axis=1).astype(str) + '-' + (WeeklyData_full.apply(lambda row: (row == 'LOSS').sum(), axis=1)).astype(str) + '-' + (WeeklyData_full.apply(lambda row: (row == 'TIE').sum(), axis=1)).astype(str)
WeeklyData_full['Points'] = WeeklyData_full.apply(lambda row: (row == 'WIN').sum(), axis=1) + (WeeklyData_full.apply(lambda row: (row == 'TIE').sum(), axis=1) * 0.5)

# Filters
with st.sidebar:  
    def reset_filters():
            st.session_state.team = "All"
            st.session_state.week = WeeklyData_full['Week'].max()
            selected_team = 'All'
            selected_week = WeeklyData_full['Week'].max()
            WeeklyData = WeeklyData_full
    st.button('Reset Filters', on_click=reset_filters)
    
    team_list = list(WeeklyData_full.Team.unique())[::-1]
    team_list.sort()
    team_list.insert(0, 'All')
    selected_team = st.selectbox('Team', team_list, index=0, key='team')
    if selected_team == 'All':
        WeeklyData = WeeklyData_full
    else:
        WeeklyData = WeeklyData_full[WeeklyData_full.Team == selected_team]

    week_list = list(WeeklyData.Week.unique())[::-1]
    week_list.append(0)
    week_list.sort()
    # If team is selected, default to week 0, else current week
    if selected_team == 'All':
        selected_week = st.selectbox('Week (select 0 for all previous)', week_list, index=len(week_list)-1, key='week')
    else:
        selected_week = st.selectbox('Week (select 0 for all previous)', week_list, index=0, key='week')
# Prepare Scoreboard Dashboard
max_week = WeeklyData['Week'].max()

if selected_week == 0:
    PreviousWeeklyData = WeeklyData[WeeklyData['Week'] != max_week]
    PreviousWeeklyData = PreviousWeeklyData.sort_values(by=['Team', 'Week'])
    columns = ['Week', 'Team', 'Record', 'R', 'HR', 'RBI', 'SB', 'OBP', 'W', 'K', 'ERA', 'WHIP', 'SVHD', 'Opponent']
    PreviousWeeklyData = PreviousWeeklyData[['Week', 'Team', 'Record', 'R_val', 'HR_val', 'RBI_val', 'SB_val', 'OBP_val', 'K_val', 'W_val', 'ERA_val', 'WHIP_val', 'SVHD_val', 'Opponent', 'Points', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD']]
    PreviousWeeklyData.columns = ['Week', 'Team', 'Record', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD', 'Opponent', 'Points', 'Ro', 'HRo', 'RBIo', 'SBo', 'OBPo', 'Ko', 'Wo', 'ERAo', 'WHIPo', 'SVHDo']
    PreviousWeeklyData.sort_values(by=['Team', 'Week'], inplace=True)
else:
    PreviousWeeklyData = WeeklyData[WeeklyData['Week'] == selected_week]
    PreviousWeeklyData = PreviousWeeklyData.drop(['Week'], axis=1)
    columns = ['Team', 'Record', 'R', 'HR', 'RBI', 'SB', 'OBP', 'W', 'K', 'ERA', 'WHIP', 'SVHD', 'Opponent']
    PreviousWeeklyData = PreviousWeeklyData[['Team', 'Record', 'R_val', 'HR_val', 'RBI_val', 'SB_val', 'OBP_val', 'K_val', 'W_val', 'ERA_val', 'WHIP_val', 'SVHD_val', 'Opponent', 'Points', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD']]
    PreviousWeeklyData.columns = ['Team', 'Record', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD', 'Opponent', 'Points', 'Ro', 'HRo', 'RBIo', 'SBo', 'OBPo', 'Ko', 'Wo', 'ERAo', 'WHIPo', 'SVHDo']
    PreviousWeeklyData.sort_values(by='Points', ascending=False, inplace=True)


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
    style_df = PreviousWeeklyData.style.apply(highlight_val, col='Ro', val_col='R', axis=1).apply(highlight_val, col='HRo', val_col='HR', axis=1)\
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
    style_df = PreviousWeeklyData.style.apply(highlight_val, col='Ro', val_col='R', axis=1).apply(highlight_val, col='HRo', val_col='HR', axis=1)\
    .apply(highlight_val, col='RBIo', val_col='RBI', axis=1).apply(highlight_val, col='SBo', val_col='SB', axis=1)\
    .apply(highlight_val, col='OBPo', val_col='OBP', axis=1).apply(highlight_val, col='Ko', val_col='K', axis=1)\
    .apply(highlight_val, col='Wo', val_col='W', axis=1).apply(highlight_val, col='ERAo', val_col='ERA', axis=1)\
    .apply(highlight_val, col='WHIPo', val_col='WHIP', axis=1).apply(highlight_val, col='SVHDo', val_col='SVHD', axis=1)\
    .apply(highlight_records, col='Points', val_col='Record', axis=1)

cols = ['R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'W', 'ERA', 'WHIP', 'SVHD']
averages = [PreviousWeeklyData[col].mean() if col in PreviousWeeklyData else np.nan for col in cols]

# Create a new DataFrame for averages
df_averages = pd.DataFrame([averages], columns=cols)
df_averages['R'] = df_averages['R'].round(0).astype(int)
df_averages['HR'] = df_averages['HR'].round(0).astype(int)
df_averages['RBI'] = df_averages['RBI'].round(0).astype(int)
df_averages['SB'] = df_averages['SB'].round(0).astype(int)
df_averages['OBP'] = df_averages['OBP'].round(3).astype(float)
df_averages['K'] = df_averages['K'].round(0).astype(int)
df_averages['W'] = df_averages['W'].round(0).astype(int)
df_averages['ERA'] = df_averages['ERA'].round(2).astype(float)
df_averages['WHIP'] = df_averages['WHIP'].round(2).astype(float)
df_averages['SVHD'] = df_averages['SVHD'].round(0).astype(int)

# Creating visuals
st.markdown('<h3 style="text-align: center;">Averages</h3>', unsafe_allow_html=True)
col = st.columns((1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
with col[0]:
    st.metric(label = 'R', value=df_averages['R'])
with col[1]:
    st.metric(label = 'HR', value=df_averages['HR'])
with col[2]:
    st.metric(label = 'RBI', value=df_averages['RBI'])
with col[3]:
    st.metric(label = 'SB', value=df_averages['SB'])
with col[4]:
    st.metric(label = 'OBP', value=df_averages['OBP'])
with col[5]:
    st.metric(label = 'W', value=df_averages['W'])
with col[6]:
    st.metric(label = 'K', value=df_averages['K'])
with col[7]:
    st.metric(label = 'ERA', value=df_averages['ERA'])
with col[8]:
    st.metric(label = 'WHIP', value=df_averages['WHIP'])
with col[9]:
    st.metric(label = 'SVHD', value=df_averages['SVHD'])

st.markdown('<h3 style="text-align: center;">Scoreboard</h3>', unsafe_allow_html=True)
st.dataframe(style_df, 
                height=457, width=2000, 
                column_order=columns,
                hide_index=True)    


