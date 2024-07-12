# Fantasy DB

import streamlit as st
import pandas as pd

data = pd.read_csv('data/FantasyData.xlsx')
st.dataframe(data)


