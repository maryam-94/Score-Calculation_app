import streamlit as st
import requests

HOST = "https://oc-projet7-api.herokuapp.com"


def predict(sk_id_curr):
    response = requests.get(HOST + '/predict/user/' + sk_id_curr)
    return response.json()


creditAccordeTemplate = """
    <div style="display: flex;" >
        <div style="width: 18%; text-align: center;">
          <i class="fa-solid {} fa-4x" style="color: {}"></i>
        </div>
        <div style="width: 75%; padding-left: 1em;">
           <b style="font-size: 17px; color: white; background-color: {}; padding: 0 0.2em; border-radius: 21px;"> {} </b>
           <div> {} </div>
           <b style="font-size: 20px; background-color: beige; padding: 0 0.4em; border-radius: 21px;"> {} </b>
        </div>
    </div>
"""


def show_client_prediction(clientDf, tab):
    col1, col2, col3 = st.columns([1, 1, 1])
    sk_id_curr = str(clientDf['SK_ID_CURR'].iloc[0])
    if col2.button('Predict Client Credit default', key=tab):
        response = predict(sk_id_curr)
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Probability of credit repayment",
                    value="%.2f" % (response['prediction']['no_default_credit_proba']* 100) + " %")
        col2.metric(label="Probability of payment difficulty",
                    value="%.2f" % (response['prediction']['default_credit_proba']* 100) + " %")
        credit_accorde = True if response['prediction']['default_credit_proba'] < response[
            'optimum_threshold'] else False
        credit_accorde_color = 'green' if credit_accorde else "red"
        credit_accorde_icon = "fa-thumbs-up" if credit_accorde else "fa-thumbs-down"
        credit_accorde_text = "CREDIT ACCEPTED" if credit_accorde else "CREDIT NOT ACCEPTED"
        credit_explain_text = 'is below threshold of: ' if credit_accorde else 'exceeds the threshold of: '
        credit_decision = creditAccordeTemplate.format(credit_accorde_icon,
                                                       credit_accorde_color,
                                                       credit_accorde_color,
                                                       credit_accorde_text,
                                                       'Probability of payment difficulty ' + credit_explain_text,
                                                       "%.2f" % (response['optimum_threshold'] * 100) + " %"
                                                       )
        col3.write(credit_decision, unsafe_allow_html=True)
