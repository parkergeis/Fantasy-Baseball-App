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

def color_win(data):
    color = 'green' if data['HR'] == 'WIN' else 'red' if data['HR'] == 'LOSS' else 'black'
    return f'<td style="color: {color}">{data["HR_val"]}</td>'

df_html = (CurrentWeeklyData.style
           .apply(lambda x: CurrentWeeklyData.apply(color_win, axis=1), subset=['HR_val'])
           .format({'HR_val': '{}'}, escape=False))

st.markdown(df_html, unsafe_allow_html=True)

st.markdown(df_html, unsafe_allow_html=True)



