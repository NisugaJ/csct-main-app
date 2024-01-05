import streamlit as st
from st_aggrid import AgGrid
import pandas as pd

def start_streamlit_app():
    st.set_page_config(page_title='AwesomeTable by @caiofaar', page_icon='📊', layout='wide')
    st.title('AwesomeTable with Search')

    st.sidebar.header('Planta')

    df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv')
    AgGrid(df)