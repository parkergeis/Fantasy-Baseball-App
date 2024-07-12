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

WeeklyData = pd.read_excel('data/FantasyData.xlsx', sheet_name='WeeklyData')
Standings = pd.read_excel('data/FantasyData.xlsx', sheet_name='PreviousStandings')
Rosters = pd.read_excel('data/FantasyData.xlsx', sheet_name='Rosters')
max_week = WeeklyData['Week'].max()
CurrentWeeklyData = WeeklyData[WeeklyData['Week'] == max_week]


st.markdown('#### Current Week')
st.dataframe(CurrentWeeklyData)



