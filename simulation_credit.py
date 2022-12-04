import streamlit as st


def simulation_credit():
    value_gender = st.selectbox('GENDER', ('male', 'female'))
    CODE_GENDER = '1' if value_gender == 'female' else '0'
    DAYS_EMPLOYED = st.text_input('DAYS_EMPLOYED')
    AMT_ANNUITY = st.text_input('CREDIT_AMOUNT')
    DAYS_BIRTH = st.text_input('DAYS_BIRTH')

    prediction = " "
    if st.button("Predict"):
        print(CODE_GENDER, DAYS_EMPLOYED, AMT_ANNUITY, DAYS_BIRTH)
        # prediction=prediction_model(CODE_GENDER, DAYS_EMPLOYED, AMT_ANNUITY, DAYS_BIRTH)
    st.success("Résultat: {}".format(prediction))
