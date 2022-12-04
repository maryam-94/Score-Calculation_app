import plotly.graph_objs as go
import streamlit as st


def show_credit_bureau_info(df_bureau_and_balance, selectedClientId):
    st.write('<i class="fa-solid fa-building-columns"></i> Credit bureau information for client:',
             unsafe_allow_html=True)
    df_bureau_and_balance_for_client = df_bureau_and_balance[df_bureau_and_balance['SK_ID_CURR'] == selectedClientId]
    if len(df_bureau_and_balance_for_client) == 0:
        st.write("""
                <div style="width: 50%; margin: 0 auto;">
                     <i class="fa-solid fa-broom"></i> 
                     There is no recoded previous Credit Bureau credit related to our loan !
                </div>
            """, unsafe_allow_html=True)
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Total credit amount (active and closed) in all credit bureau:",
                      value="%.2f" % df_bureau_and_balance_for_client['BURO_AMT_CREDIT_SUM_SUM'])
            pie = go.Figure(data=[go.Pie(hole=.3,
                                         labels=['Total Active credits amount', 'Total Closed credits amount'],
                                         values=["%.2f" % df_bureau_and_balance_for_client['ACTIVE_AMT_CREDIT_SUM_SUM'],
                                                 "%.2f" % df_bureau_and_balance_for_client[
                                                     'CLOSED_AMT_CREDIT_SUM_SUM']])])

            pie.update_traces(hoverinfo='label+percent',
                              textinfo='percent+value',
                              textfont_size=20,
                              marker=dict(colors=['gold', 'mediumturquoise', 'darkorange', 'lightgreen'],
                                          line=dict(color='#000000', width=2)))
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

            remainingDebtSummary = remainingDebtTemplate.format(
                "%.2f" % df_bureau_and_balance_for_client['ACTIVE_AMT_CREDIT_SUM_DEBT_SUM'],
                "%.2f" % ((float(df_bureau_and_balance_for_client['ACTIVE_AMT_CREDIT_SUM_DEBT_SUM']) / float(
                    df_bureau_and_balance_for_client['ACTIVE_AMT_CREDIT_SUM_SUM'])) * 100),
                "%.2f" % df_bureau_and_balance_for_client['ACTIVE_AMT_CREDIT_SUM_SUM'],
                "%.0f" % df_bureau_and_balance_for_client['ACTIVE_DAYS_CREDIT_ENDDATE_MAX'])
            st.write(remainingDebtSummary, unsafe_allow_html=True)

            pie = go.Figure(data=[go.Pie(labels=['Total remaining debt', 'Total paid debt'],
                                         values=[
                                             float(df_bureau_and_balance_for_client['ACTIVE_AMT_CREDIT_SUM_DEBT_SUM']),
                                             float(
                                                 df_bureau_and_balance_for_client['ACTIVE_AMT_CREDIT_SUM_SUM']) - float(
                                                 df_bureau_and_balance_for_client['ACTIVE_AMT_CREDIT_SUM_DEBT_SUM'])
                                         ],
                                         pull=[0, 0.2])])

            pie.update_traces(hoverinfo='label+percent',
                              textinfo='percent+value',
                              textfont_size=20,
                              marker=dict(colors=['darkorange', 'gold'], line=dict(color='#000000', width=2)))
            st.plotly_chart(pie, use_container_width=True)

        with st.expander("bureau and balance:"):
            st.write(df_bureau_and_balance_for_client)
