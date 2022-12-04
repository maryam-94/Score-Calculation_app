from load_data import load_data, load_bureau_and_balance
from search_client_forms import *
from show_client_application_info import *
from show_credit_bureau_info import *
from simulation_credit import *

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

df = load_data()
df_bureau_and_balance = load_bureau_and_balance()

# ----- BEGIN : MAIN CODE -----
with st.container():
    tab1, tab2, tab3 = st.tabs(["Basic Search", "Advanced Search", "Simulation credit"])

    with tab1:
        selectedClientId1 = commun_search_client_form(df)
        show_client_application_info(df, selectedClientId1)
        show_credit_bureau_info(df_bureau_and_balance, selectedClientId1)
    with tab2:
        selectedClientId2 = advanced_search_client_form(df)
        show_client_application_info(df, selectedClientId2)
        show_credit_bureau_info(df_bureau_and_balance, selectedClientId2)
    with tab3:
        simulation_credit()
    #     pie = go.Figure(data=[go.Pie(labels = df['NAME_EDUCATION_TYPE'].value_counts().keys(),
    #                                  values = df['NAME_EDUCATION_TYPE'].value_counts().values)])
    #
    #     st.plotly_chart(pie, use_container_width=True)

# ----- END : MAIN CODE -----
