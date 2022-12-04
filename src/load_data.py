import streamlit as st
import pandas as pd

# ----- BEGIN : load_data -----
@st.cache
def load_data():
    data = pd.read_pickle(r'data/data_for_dashboard.pickle')
    data.reset_index(drop=True, inplace=True)
    # data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')
    return data

@st.cache
def load_bureau_and_balance():
    data = pd.read_pickle(r'data/bureau_for_app.pickle')
    data.reset_index(drop=False, inplace=True)
    # data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')
    return data

# @st.cache
# def load_columns_description():
#     df_columns_description_path = "data/HomeCredit_columns_description.csv"
#     return pd.read_csv(df_columns_description_path, encoding='latin')
#
# df_columns_description = load_columns_description()
# # st.write('df_columns_description', df_columns_description)
# df_columns_description[df_columns_description['Row'] == 'AMT_CREDIT_SUM_DEBT']
# ----- END : load_data -----
