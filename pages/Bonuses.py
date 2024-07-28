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

max_week = WeeklyData['Week'].max()
WeeklyData = WeeklyData[WeeklyData['Week'] != max_week]
WeeklyData['Record'] = WeeklyData.apply(lambda row: (row == 'WIN').sum(), axis=1).astype(str) + '-' + (WeeklyData.apply(lambda row: (row == 'LOSS').sum(), axis=1)).astype(str) + '-' + (WeeklyData.apply(lambda row: (row == 'TIE').sum(), axis=1)).astype(str)
WeeklyData['Points'] = WeeklyData.apply(lambda row: (row == 'WIN').sum(), axis=1) + (WeeklyData.apply(lambda row: (row == 'TIE').sum(), axis=1) * 0.5)


# Assuming WeeklyData is a pandas DataFrame
# First, find the maximum points for each week
max_points_per_week = WeeklyData.groupby('Week')['Points'].max()

# Create a boolean mask for rows where 'Points' is the maximum for the 'Week'
mask = WeeklyData.groupby('Week')['Points'].transform(max) == WeeklyData['Points']

# Apply the mask to the DataFrame to get only the rows with the maximum 'Points' for each 'Week'
WeeklyWinners_max = WeeklyData[mask]

# Then, count the number of times the maximum points occur for each week
counts = WeeklyWinners_max.groupby('Week').size()

# Create a new column 'Prize' and initialize it with $5
WeeklyWinners_max['Prize'] = 5

# Find the weeks where the maximum points occur more than once
weeks_with_multiple_max = counts[counts > 1].index

# For these weeks, set the 'Prize' to 0
WeeklyWinners_max.loc[WeeklyWinners_max['Week'].isin(weeks_with_multiple_max), 'Prize'] = 0

# Create a new column 'Rollover' and initialize it with 0
WeeklyWinners_max['Rollover'] = 0

# For weeks after a week with multiple max, add the rollover amount
rollover = 0
for week in sorted(WeeklyWinners_max['Week'].unique()):
    if week in weeks_with_multiple_max:
        rollover += 5
    else:
        WeeklyWinners_max.loc[WeeklyWinners_max['Week'] == week, 'Rollover'] = rollover
        rollover = 0

# Add the 'Rollover' to the 'Prize'
WeeklyWinners_max['Prize'] += WeeklyWinners_max['Rollover']

# Drop the 'Rollover' column as it's no longer needed
WeeklyWinners_max = WeeklyWinners_max.drop(columns='Rollover')

WeeklyWinners = WeeklyWinners_max[['Week', 'Team', 'Record', 'Prize']]
WeeklyWinners.columns = ['Week', 'Team', 'Record', '$']

TotalPrizes_test = WeeklyWinners[['Team', '$']]
TotalPrizes = TotalPrizes_test.groupby(by='Team').sum()
TotalPrizes['Wins'] = TotalPrizes_test.groupby(by='Team').count()
TotalPrizes.sort_values(by=['$', 'Wins'], ascending=False,inplace=True)
TotalPrizes.reset_index(inplace=True)

col = st.columns((4, 4), gap='medium')
with col[0]:
    st.markdown('<h3 style="text-align: center;">Weekly Winners</h3>', unsafe_allow_html=True)
    st.dataframe(WeeklyWinners, hide_index=True)

with col[1]:
    st.markdown('<h3 style="text-align: center;">Winnings</h3>', unsafe_allow_html=True)
    st.dataframe(TotalPrizes,
                column_order=("Team", "$", "Wins"),
                hide_index=True,
                width=None,
                column_config={
                "Team": st.column_config.TextColumn(
                    "Team",
                ),
                "Wins": st.column_config.TextColumn(
                    "Wins",
                ),
                "$": st.column_config.ProgressColumn(
                    "$",
                    format="%f",
                    min_value=0,
                    max_value=(max(WeeklyWinners.Week)-1)*5,
                    )}
                )


