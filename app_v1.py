import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import altair as alt
from datetime import datetime
import plotly.express as px  # interactive charts
import plotly.figure_factory as ff
import plotly.graph_objs as go
from plotly.offline import iplot

st.set_page_config(
    page_title="Dashboard",
    page_icon="✅",
    layout="wide",
)

# dashboard title
st.title('Dashboard interactif pour la société < Prêt à dépenser > ')
# st.markdown("<h2 style='text-align: center; color: green;'> Dashboard interactif pour la société Prêt à dépenser  </h2>", unsafe_allow_html=True)





@st.cache
def load_data():
    data = pd.read_pickle(r'./data_for_dashboard.pickle')
    data.reset_index(drop=True, inplace=True)
    # data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')
    return data
df = load_data()

# top-level filters
# Gender_filter = st.selectbox("Select the Gender", pd.unique(df['CODE_GENDER_y']))

# show data on streamlit
# st.write(df)
# st.table(data=df)
# st.dataframe(df.drop_duplicates(subset=['SK_ID_CURR']).set_index('SK_ID_CURR').filter(items=['SK_ID_CURR', 'CODE_GENDER_y', 'NAME_EDUCATION_TYPE']))
st.header('Select a client from list below')
selectClientDf = df.drop_duplicates(subset=['SK_ID_CURR']).filter(items=['SK_ID_CURR', 'CODE_GENDER_y', 'NAME_EDUCATION_TYPE'])
selectClientDf["SELECT_BOX_TEXT"] = selectClientDf['SK_ID_CURR'].astype(str) + "(gender:" + selectClientDf["CODE_GENDER_y"]+", education: "+ selectClientDf["NAME_EDUCATION_TYPE"] + ")"
selectedText = st.selectbox('Select client id', list(selectClientDf["SELECT_BOX_TEXT"]))

selectedClientId = selectClientDf[selectClientDf['SELECT_BOX_TEXT'] == selectedText]['SK_ID_CURR'].iloc[0]
st.write('You selected:', selectedClientId)
st.write('You selected:', df[df['SK_ID_CURR'] == selectedClientId])
clientDf = df[df['SK_ID_CURR'] == selectedClientId]

col1, col2, col3 = st.columns(3)
col1.metric(label="probabilité que le client rembourse son crédit", value= "%.2f" % clientDf['predict_proba_0'])
col2.metric(label="probabilité que le client ne rembourse pas son crédit", value= "%.2f" % clientDf['predict_proba_1'])
col3.metric(label="Difficulté de paiement", value= int(clientDf['y_pred']))
# with col2:
#     st.write('You selected:', clientDf['CREDIT_ACTIVE'].value_counts())

# st.metric(label="Credits actifs", value= clientDf[clientDf['CREDIT_ACTIVE'] == 'Active'].value_counts().astype(str) + "/" + str(len(clientDf)))
st.header('Filter on clients by:')

# create two columns for charts
fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.markdown("### First Chart")
    # fig = px.density_heatmap(
    #     data_frame=df, y='AMT_CREDIT', x='CODE_GENDER_y'
    # )
    # st.write(fig)

    fig = ff.create_distplot([df[df['CODE_GENDER_y'] == 'F']['AMT_CREDIT'],
                              df[df['CODE_GENDER_y'] == 'M']['AMT_CREDIT']],
                             ['GENDER=> F', 'GENDER=> M'],
                             bin_size=[2, 2],
                             show_rug=False,
                             show_hist=False,
                             show_curve=True
                             )
    fig.update_layout(autosize=False,
    width=600,
    height=400,


    xaxis=dict(title='Montant crédit'),
                      yaxis=dict(title='Density'),
                      barmode='overlay')
    st.write(fig)

#
with fig_col2:
    st.markdown("### Second Chart")
    fig2 = px.histogram(data_frame=df, x='NAME_INCOME_TYPE')
    st.write(fig2)


st.subheader('Third chart')
pie = go.Figure(data=[go.Pie(labels = df['NAME_EDUCATION_TYPE'].value_counts().keys(),
                             values = df['NAME_EDUCATION_TYPE'].value_counts().values)])

st.write(pie)