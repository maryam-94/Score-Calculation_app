import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import altair as alt
from datetime import datetime



# DATA_URL = ('bureau.csv')
@st.cache
def load_data():
    data = pd.read_pickle(r'C:\Users\chouc\openclassrooms\projet7\X_final1.pickle')
    # data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')
    return data
df = load_data()

# show data on streamlit
st.write(df)
