import streamlit as st
import pandas as pd
import uuid
from datetime import date, datetime
import io

inv_dict = {'No Invoice': ['493707800006202406','493707800006202402',\
                           '493753200006202308','493753100006202307',\
                            '412207800006201905'],
            'Nominal (Rp)': [3000000,7000000,1000000,2000000,8000000],
            'Company': ['PT KAI','PT PLN','Astra','United Tractor','PT Dirgantara'],
            'Id Pelanggan': ['4937078','4937078','4937532','4937531','4122078'],
            'Is Paid': [True, True, False, False, False],
            'Payment Id':[uuid.uuid4(),uuid.uuid4(),None,None,None],
            'Payment Due Date': [date(2024,6,30),date(2024,2,29),date(2023,8,30),date(2023,7,30),date(2019,5,30)],
            'Payment Date':[date(2024,6,13),date(2024,2,4),None,None,None]}
inv_df = pd.DataFrame(inv_dict)
st.session_state.inv_df = pd.DataFrame(inv_dict)
buffer = io.BytesIO()

st.set_page_config(layout="wide")
st.title("Automation Payment Verification (Real-Time)")
st.write("Tabel Status Invoice")
placeholder = st.empty()
placeholder.dataframe(st.session_state.inv_df)

col1, col2 = st.columns(2)

col1.header("Input Data Invoice")
in_inv = col1.text_input("Invoice No")
in_nom = col1.text_input("Nominal (Rp)")
in_company = col1.text_input("Company")
in_id_comp = col1.text_input("Id Company")
in_date = col1.date_input("Date Invoice")

if st.button("Submit",type='primary'):
    st.success("Data is Submitted")
    print('len:', len(st.session_state.inv_df))
    st.session_state.inv_df.loc[len(st.session_state.inv_df)] = {'No Invoice':str(in_inv),'Nominal (Rp)':int(in_nom),'Company':str(in_company), \
                                                                 'Id Pelanggan':str(in_id_comp), 'Payment Id': None, 'Is Paid': False,\
                                                                'Payment Due Date':in_date}
    print('st.session_state.inv_df: ', st.session_state.inv_df)
    placeholder.empty()
    placeholder.dataframe(st.session_state.inv_df)

col2.header("Form Simulasi Pembayaran")
pay_va = col2.text_input("Sim No Invoice")
if col2.button("Pay",type='primary'):
    col2.warning("Payment is sent!")
    sim_df = inv_df[inv_df['No Invoice'] == pay_va].head(1)
    print(sim_df)
    if len(sim_df)>0 and sim_df['Is Paid'].values[0] == False :# and sim_df['Nominal (Rp)'].values[0] == int(pay_nom) :
        inv_df.loc[sim_df.index,'Is Paid'] = True
        inv_df.loc[sim_df.index,'Payment Id'] = uuid.uuid4()
        inv_df.loc[sim_df.index,'Payment Date'] = datetime.now()

        col2.success("Payment is Received! Email is sent")
        placeholder.empty()
        placeholder.dataframe(inv_df)
    else:
        col2.error("No Invoice is matched")

col2.header('Download Rekap')
col2.download_button(
   "Download",
   st.session_state.inv_df[st.session_state.inv_df['Is Paid']].to_csv(index=False).encode('utf-8'),
   "rekap.csv",
   "text/csv",
   key='download-csv'
)