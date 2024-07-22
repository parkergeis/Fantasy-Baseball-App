# Fantasy DB - Overall Ranks

# Add weekly winners, overviews, legacy + rosters
# Add maybe some cool visuals

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Fantasy Dashboard",
    layout="wide")

# Import data - needs manually uploaded and committed to GitHub
WeeklyData = pd.read_excel('data/FantasyData.xlsx', sheet_name='WeeklyData')

st.markdown('<h3 style="text-align: center;">Season Scoreboard</h3>', unsafe_allow_html=True)
container = st.container()
with container:
    st.write("")
        
# st.write("") # Use to add gaps


