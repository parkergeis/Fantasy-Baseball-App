# example/st_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection

url = "hhttps://docs.google.com/spreadsheets/d/1DO97mLDDqkgq-QoQCuXgJfRefyocmHSI1-OJxBafR6U/edit?gid=0#gid=0"

conn = st.experimental_connection("gsheets", type=GSheetsConnection)

data = conn.read(spreadsheet=url, usecols=[0, 1])
st.dataframe(data)