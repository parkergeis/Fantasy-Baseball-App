# Fantasy DB

import streamlit as st
import pandas as pd

data = pd.read_excel('data/FantasyData.xlsx')
st.dataframe(data)


