
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import altair as alt
from datetime import datetime

print('hello maryam')
chart_data = pd.DataFrame(
    np.random.randn(50, 3),
    columns=["a", "b", "c"])

st.bar_chart(chart_data)
