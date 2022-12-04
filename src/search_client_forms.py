import streamlit as st
import pandas as pd

# ----- BEGIN : commun_search_client_form -----
def commun_search_client_form(df):
    selectClientDf = df.filter(items=['SK_ID_CURR', 'CODE_GENDER_y', 'NAME_EDUCATION_TYPE'])
    selectClientDf["SELECT_BOX_TEXT"] = selectClientDf['SK_ID_CURR'].astype(str) + "(gender:" + selectClientDf[
        "CODE_GENDER_y"] + ", education: " + selectClientDf["NAME_EDUCATION_TYPE"] + ")"
    selectboxList = list(selectClientDf["SELECT_BOX_TEXT"])
    selectedText = st.selectbox('Select client id', selectboxList)
    selectedClientId1 = selectClientDf[selectClientDf['SELECT_BOX_TEXT'] == selectedText]['SK_ID_CURR'].iloc[0]
    return selectedClientId1
# ----- END : commun_search_client_form -----

# ----- BEGIN : advanced_search_client_form -----
def advanced_search_client_form(df):
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
# ----- END : advanced_search_client_form -----
