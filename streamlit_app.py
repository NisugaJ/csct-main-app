import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
import numpy as np

st.set_page_config(page_title="Home", page_icon='🌱', layout='wide', menu_items={
    'Get Help': 'https://www.extremelycoolapp.com/help',
    'Report a bug': "https://www.extremelycoolapp.com/bug",
    'About': "# This is a header. This is an *extremely* cool app!"
})

sidebar = st.sidebar
sidebar.title(':green[Planta]', anchor=False)
sidebar.write(':grey[Affordable plant based food better than meat]')


# df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv')
# AgGrid(df)

