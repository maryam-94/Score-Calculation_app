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
st.write('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"> ',
         unsafe_allow_html=True)


# ----- BEGIN : load_data -----
@st.cache
def load_data():
    data = pd.read_pickle(r'./data_for_dashboard.pickle')
    data.reset_index(drop=True, inplace=True)
    # data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')
    return data
df = load_data()
# ----- END : load_data -----


# ----- BEGIN : communSearchClient -----
def communSearchClient():
    selectClientDf = df.filter(items=['SK_ID_CURR', 'CODE_GENDER_y', 'NAME_EDUCATION_TYPE'])
    selectClientDf["SELECT_BOX_TEXT"] = selectClientDf['SK_ID_CURR'].astype(str) + "(gender:" + selectClientDf[
        "CODE_GENDER_y"] + ", education: " + selectClientDf["NAME_EDUCATION_TYPE"] + ")"
    selectboxList = list(selectClientDf["SELECT_BOX_TEXT"])
    selectedText = st.selectbox('Select client id', selectboxList)
    selectedClientId1 = selectClientDf[selectClientDf['SELECT_BOX_TEXT'] == selectedText]['SK_ID_CURR'].iloc[0]
    print('client id in commun search', selectedClientId1)
    return selectedClientId1
# ----- END : communSearchClient -----

# ----- BEGIN : advancedSearchClient -----
def advancedSearchClient():
    filter1 = {
        'label': "Select the Gender",
        'column': 'CODE_GENDER_y'
    }
    filter2 = {
        'label': "Select Education type",
        'column': 'NAME_EDUCATION_TYPE'
    }
    col1, col2, col3 = st.columns(3)
    selectedFilter1 = col1.radio(filter1['label'], pd.unique(df[filter1['column']]))
    selectFilter2 = col2.selectbox(filter2['label'],
                                   pd.unique(df[df[filter1['column']] == selectedFilter1][filter2['column']]))
    selectedClientId2 = col3.selectbox('Select client id', pd.unique(
        df[(df[filter1['column']] == selectedFilter1) & (df[filter2['column']] == selectFilter2)]['SK_ID_CURR']))
    print('client id in advanced search', selectedClientId2)
    return selectedClientId2
# ----- END : advancedSearchClient -----

# ----- BEGIN : showSelectedClientInfo -----
def showSelectedClientInfo(selectedClientId):
    # Search results
    st.write('<i class="fa-solid fa-square-poll-horizontal"></i> Client application data :', unsafe_allow_html=True)
    # selectedClient
    clientDf = df[df['SK_ID_CURR'] == selectedClientId]

    # gender icon
    clientInfoTemplate = """
    <div style="display: flex;" >
        <div style="width: 18%; text-align: center;">
          <i class="fa-solid {} fa-5x"></i>
        </div>
        <div style="width: 75%; padding-left: 1em;">
           <b style="background-color: aliceblue; padding: 0 0.2em; border-radius: 21px;"> {} </b>
           <div> {} </div>
           <div> {} </div>
        </div>
    </div>
    """

    gender = "Female" if clientDf['CODE_GENDER_y'].iloc[0] == 'F' else "Male"
    gender_icon = "fa-person-dress" if clientDf['CODE_GENDER_y'].iloc[0] == 'F' else "fa-person"
    clientInfo = clientInfoTemplate.format(gender_icon, str(selectedClientId), gender, clientDf['NAME_EDUCATION_TYPE'].iloc[0])

    col1, col2, col3 = st.columns(3)
    col1.write(clientInfo, unsafe_allow_html=True)
    col2.metric(label=clientDf['NAME_INCOME_TYPE'].iloc[0], value= "%.0f" % clientDf['AMT_INCOME_TOTAL'].iloc[0])
    col3.metric(label="Credit Amount", value= int(clientDf['AMT_CREDIT']))

    col1, col2, col3 = st.columns(3)
    col1.metric(label="probabilité que le client rembourse son crédit", value= "%.4f" % clientDf['predict_proba_0'])
    col2.metric(label="probabilité que le client ne rembourse pas son crédit", value= "%.4f" % clientDf['predict_proba_1'])
    col3.metric(label="Difficulté de paiement", value= int(clientDf['y_pred']))

    with st.expander("See More:"):
        st.write(df[df['SK_ID_CURR'] == selectedClientId])

# ----- END : showSelectedClientInfo -----


# ----- BEGIN : MAIN CODE -----
with st.container():
    tab1, tab2 = st.tabs(["Basic Search", "Advanced Search"])

    with tab1:
        selectedClientId1 = communSearchClient()
        showSelectedClientInfo(selectedClientId1)
    with tab2:
        selectedClientId2 = advancedSearchClient()
        showSelectedClientInfo(selectedClientId2)

st.markdown("""---""")

with st.container():
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

# ----- END : MAIN CODE -----