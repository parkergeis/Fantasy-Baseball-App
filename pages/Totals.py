# Fantasy DB - Totals

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Fantasy Dashboard",
    layout="wide",
    initial_sidebar_state="auto")

# Import data - needs manually uploaded and committed to GitHub
WeeklyData = pd.read_excel('data/FantasyData.xlsx', sheet_name='WeeklyData')

st.markdown('<h3 style="text-align: center;">H2H Totals</h3>', unsafe_allow_html=True)
container = st.container()
with container:
    st.write("")


