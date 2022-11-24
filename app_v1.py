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

# @st.cache
# def load_columns_description():
#     df_columns_description_path = "data/HomeCredit_columns_description.csv"
#     return pd.read_csv(df_columns_description_path, encoding='latin')
#
# df_columns_description = load_columns_description()
# # st.write('df_columns_description', df_columns_description)
# df_columns_description[df_columns_description['Row'] == 'AMT_CREDIT_SUM_DEBT']

# ----- BEGIN : load_data -----
@st.cache
def load_data():
    data = pd.read_pickle(r'./data/data_for_dashboard.pickle')
    data.reset_index(drop=True, inplace=True)
    # data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')
    return data
df = load_data()

# ----- END : load_data -----

@st.cache
def load_bureau_and_balance():
    data = pd.read_pickle(r'./data/bureau_for_app.pickle')
    data.reset_index(drop=False, inplace=True)
    # data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')
    return data
df_bureau_and_balance = load_bureau_and_balance()
# st.write('df_bureau_and_balance', df_bureau_and_balance.head())

# ----- BEGIN : communSearchClient -----
def communSearchClient():
    selectClientDf = df.filter(items=['SK_ID_CURR', 'CODE_GENDER_y', 'NAME_EDUCATION_TYPE'])
    selectClientDf["SELECT_BOX_TEXT"] = selectClientDf['SK_ID_CURR'].astype(str) + "(gender:" + selectClientDf[
        "CODE_GENDER_y"] + ", education: " + selectClientDf["NAME_EDUCATION_TYPE"] + ")"
    selectboxList = list(selectClientDf["SELECT_BOX_TEXT"])
    selectedText = st.selectbox('Select client id', selectboxList)
    selectedClientId1 = selectClientDf[selectClientDf['SELECT_BOX_TEXT'] == selectedText]['SK_ID_CURR'].iloc[0]
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
          <i class="fa-solid {} fa-6x"></i>
        </div>
        <div style="width: 75%; padding-left: 1em;">
           <b style="font-size: 28px; background-color: aliceblue; padding: 0 0.2em; border-radius: 21px;"> {} </b>
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
    incomeTemplate = """
    <div data-testid="metric-container">
        <label data-testid="stMetricLabel" class="css-186pv6d e16fv1kl2">
            <div class="css-50ug3q e16fv1kl3">
                Income of the client as 
                <b style="background-color: aliceblue; padding: 0 0.2em; border-radius: 21px;"> {} </b>:
            </div>
        </label>
        <div data-testid="stMetricValue" class="css-1xarl3l e16fv1kl1">
            <div class="css-50ug3q e16fv1kl3"> {} </div>
        </div>
        <label data-testid="stMetricLabel" class="css-186pv6d e16fv1kl2">
            <div class="css-50ug3q e16fv1kl3">
                Average income for same type is
                <b style="background-color: aliceblue; padding: 0 0.2em; border-radius: 21px;"> {} </b>
            </div>
        </label>
    </div>
    """
    col2.write(
        incomeTemplate.format(
            clientDf['NAME_INCOME_TYPE'].iloc[0],
            "%.0f" % clientDf['AMT_INCOME_TOTAL'].iloc[0],
            "%.0f" % df[df['NAME_INCOME_TYPE']== clientDf['NAME_INCOME_TYPE'].iloc[0]]["AMT_INCOME_TOTAL"].mean()
        ),
        unsafe_allow_html=True
    )
    col3.metric(label="Credit Amount", value= int(clientDf['AMT_CREDIT']))
    st.empty()
    col1, col2, col3 = st.columns(3)
    col1.metric(label="probabilité que le client rembourse son crédit", value= "%.4f" % clientDf['predict_proba_0'])
    col2.metric(label="probabilité que le client ne rembourse pas son crédit", value= "%.4f" % clientDf['predict_proba_1'])
    col3.metric(label="Difficulté de paiement", value= int(clientDf['y_pred']))

    with st.expander("See More:"):
        st.write(df[df['SK_ID_CURR'] == selectedClientId])

    st.write('<i class="fa-solid fa-building-columns"></i> Credit bureau information for client:', unsafe_allow_html=True)
    df_bureau_and_balance_for_client = df_bureau_and_balance[df_bureau_and_balance['SK_ID_CURR'] == selectedClientId]
    if len(df_bureau_and_balance_for_client) == 0 :
        st.write("""
            <div style="width: 50%; margin: 0 auto;">
                 <i class="fa-solid fa-broom"></i> 
                 There is no recoded previous Credit Bureau credit related to our loan !
            </div>
        """, unsafe_allow_html=True)
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Total credit amount (active and closed) in all credit bureau:", value= "%.2f" % df_bureau_and_balance_for_client['BURO_AMT_CREDIT_SUM_SUM'])
            pie = go.Figure(data=[go.Pie(hole=.3,
                                         labels = ['Total Active credits amount', 'Total Closed credits amount'],
                                         values = [ "%.2f" % df_bureau_and_balance_for_client['ACTIVE_AMT_CREDIT_SUM_SUM'],  "%.2f" % df_bureau_and_balance_for_client['CLOSED_AMT_CREDIT_SUM_SUM']])])

            pie.update_traces(hoverinfo='label+percent',
                              textinfo='percent+value',
                              textfont_size=20,
                              marker=dict(colors=['gold', 'mediumturquoise', 'darkorange', 'lightgreen'], line=dict(color='#000000', width=2)))
            st.plotly_chart(pie, use_container_width=True)

        with col2:
            remainingDebtTemplate = """
            <div data-testid="metric-container">
                <label data-testid="stMetricLabel" class="css-186pv6d e16fv1kl2">
                    <div class="css-50ug3q e16fv1kl3">Total remaining debt:</div>
                </label>
                <div data-testid="stMetricValue" class="css-1xarl3l e16fv1kl1">
                    <div class="css-50ug3q e16fv1kl3"> {} </div>
                </div>
                <label data-testid="stMetricLabel" class="css-186pv6d e16fv1kl2">
                    <div class="css-50ug3q e16fv1kl3">
                        represents
                        <b style="background-color: #ff8c00a3; padding: 0 0.2em; border-radius: 21px;"> {}%</b>
                        of active current total credit amount 
                        <b style="background-color: #ffe24794; padding: 0 0.2em; border-radius: 21px;"> {} </b>,
                        to pay in 
                        <b style="background-color: aliceblue; padding: 0 0.2em; border-radius: 21px;"> {} </b>
                        Days
                    </div>
                </label>
            </div>
            """

            remainingDebtSummary = remainingDebtTemplate.format("%.2f" % df_bureau_and_balance_for_client['ACTIVE_AMT_CREDIT_SUM_DEBT_SUM'],
                                                                "%.2f" % ((float(df_bureau_and_balance_for_client['ACTIVE_AMT_CREDIT_SUM_DEBT_SUM']) / float(df_bureau_and_balance_for_client['ACTIVE_AMT_CREDIT_SUM_SUM'])) * 100),
                                                                "%.2f" % df_bureau_and_balance_for_client['ACTIVE_AMT_CREDIT_SUM_SUM'],
                                                                "%.0f" % df_bureau_and_balance_for_client['ACTIVE_DAYS_CREDIT_ENDDATE_MAX'])
            st.write(remainingDebtSummary, unsafe_allow_html=True)

            pie = go.Figure(data=[go.Pie(labels = ['Total remaining debt', 'Total paid debt'],
                                         values = [ float(df_bureau_and_balance_for_client['ACTIVE_AMT_CREDIT_SUM_DEBT_SUM']),
                                                    float(df_bureau_and_balance_for_client['ACTIVE_AMT_CREDIT_SUM_SUM']) - float(df_bureau_and_balance_for_client['ACTIVE_AMT_CREDIT_SUM_DEBT_SUM'])
                                                    ],
                                         pull=[0, 0.2])])

            pie.update_traces(hoverinfo='label+percent',
                              textinfo='percent+value',
                              textfont_size=20,
                              marker=dict(colors=['darkorange', 'gold'], line=dict(color='#000000', width=2)))
            st.plotly_chart(pie, use_container_width=True)

        with st.expander("bureau and balance:"):
            st.write(df_bureau_and_balance_for_client)


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
        st.plotly_chart(fig, use_container_width=True)
    #
    with fig_col2:
        st.markdown("### Second Chart")
        fig2 = px.histogram(data_frame=df, x='NAME_INCOME_TYPE')
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader('Third chart')
    pie = go.Figure(data=[go.Pie(labels = df['NAME_EDUCATION_TYPE'].value_counts().keys(),
                                 values = df['NAME_EDUCATION_TYPE'].value_counts().values)])

    st.plotly_chart(pie, use_container_width=True)

# ----- END : MAIN CODE -----