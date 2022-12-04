import streamlit as st
import plotly.express as px  # interactive charts
import plotly.figure_factory as ff
import plotly.graph_objs as go

# ----- BEGIN : show_client_application_info -----
def show_client_application_info(df, selectedClientId):
    st.write('<i class="fa-solid fa-square-poll-horizontal"></i> Client application data :', unsafe_allow_html=True)
    clientDf = df[df['SK_ID_CURR'] == selectedClientId]

    show_client_personal_info(df, clientDf, selectedClientId)
    st.empty()
    show_client_chart_comparison(df, clientDf['NAME_EDUCATION_TYPE'].iloc[0])
    show_client_prediction_results(clientDf)
    with st.expander("See More:"):
        st.write(df[df['SK_ID_CURR'] == selectedClientId])
# ----- END : show_client_application_info -----


def show_client_personal_info(df, clientDf, selectedClientId):
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
    clientInfo = clientInfoTemplate.format(gender_icon, str(selectedClientId), gender,
                                           clientDf['NAME_EDUCATION_TYPE'].iloc[0])

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
            "%.0f" % df[df['NAME_INCOME_TYPE'] == clientDf['NAME_INCOME_TYPE'].iloc[0]]["AMT_INCOME_TOTAL"].mean()
        ),
        unsafe_allow_html=True
    )
    col3.metric(label="Credit Amount", value=int(clientDf['AMT_CREDIT']))

def show_client_prediction_results(clientDf):
    col1, col2, col3 = st.columns(3)
    col1.metric(label="probabilité que le client rembourse son crédit", value="%.4f" % clientDf['predict_proba_0'])
    col2.metric(label="probabilité que le client ne rembourse pas son crédit",
                value="%.4f" % clientDf['predict_proba_1'])
    col3.metric(label="Difficulté de paiement", value=int(clientDf['y_pred']))

def show_client_chart_comparison(df, clientEducationType):
    fig_col1, fig_col2, fig_col3 = st.columns(3)
    with fig_col1:
        df_education_type_count = df['NAME_EDUCATION_TYPE'].value_counts()
        labels = df_education_type_count.index.tolist()
        values = df_education_type_count.values.tolist()
        clientValueIndex = labels.index(clientEducationType)
        pull = [0] * len(labels)
        pull[clientValueIndex] = 0.2
        pie = go.Figure(data=[go.Pie(labels=labels, values=values, pull=pull)])

        pie.update_layout(margin=dict(l=20, r=20, t=60, b=20),
                          legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=1.02,
                              xanchor="right",
                              x=1
                          )
                          )
        pie.update_traces(hoverinfo='label+percent',
                          marker=dict(colors=['gold', 'mediumturquoise', 'darkorange', 'lightgreen']))
        st.plotly_chart(pie, use_container_width=True)
    with fig_col2:
        df_mean = df[['NAME_INCOME_TYPE', 'AMT_INCOME_TOTAL', 'AMT_CREDIT']].groupby('NAME_INCOME_TYPE').mean()
        df_mean.reset_index(drop=False, inplace=True)
        fig2 = px.histogram(data_frame=df_mean,
                            x='NAME_INCOME_TYPE',
                            y='AMT_INCOME_TOTAL',
                            title='Average income per type for all clients',
                            labels={'NAME_INCOME_TYPE': 'Income Type', 'AMT_INCOME_TOTAL': 'Average income'}
                            ).update_layout(margin=dict(l=20, r=20, t=60, b=20),
                                            yaxis_title="Average income")
        st.plotly_chart(fig2, use_container_width=True)

    with fig_col3:
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
                          margin=dict(l=20, r=20, t=20, b=20),
                          # width=600,
                          # height=400,
                          legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=1.02,
                              xanchor="right",
                              x=1
                          ),
                          xaxis=dict(title='Montant crédit'),
                          yaxis=dict(title='Density'),
                          barmode='overlay')
        st.plotly_chart(fig, use_container_width=True)
