import streamlit as st
import pandas as pd
import uuid
from datetime import date, datetime

inv_dict = {'No Invoice': ['493217800006202406','493707800006202402',\
                           '493753200006202308','493707800006202307',\
                           '412207800006202203','225120780006202201',\
                            '412207800006201905','493753280006201602'],
            'Nominal (Rp)': [3000000,7000000,15000000,4300000,1000000,2000000,8000000,7500000],
            'Company': ['PT KAI','PT PLN','Astra','PT PLN','PT Dirgantara','United Tractor','PT Dirgantara','Astra'],
            'Id Pelanggan': ['4932178','4937078','4937532','4937078','4122078','2251207','4122078','4937532'],
            'Is Paid': [True, True, False, False, False,False, True, True],
            'Payment Id':[uuid.uuid4(),uuid.uuid4(),None,None,None,None,uuid.uuid4(),uuid.uuid4()],
            'Payment Due Date': [date(2024,6,30),date(2024,2,29),date(2023,8,30),date(2023,7,30),date(2022,3,30),date(2022,1,30),date(2019,5,30),date(2016,2,28)],
            'Payment Date':[datetime(2024,6,13,17,9,13),datetime(2024,2,4,13,5,12),None,None,None,None, datetime(2019,5,2,8,31,13),datetime(2016,2,6,21,51,16)]}

inv_df = pd.DataFrame(inv_dict)
st.session_state.inv_df = pd.DataFrame(inv_dict)

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>MyDigiFlag : Automatic Payment Verification</h1>", unsafe_allow_html=True)
st.write("Tabel Status Invoice")
placeholder = st.empty()
placeholder.dataframe(st.session_state.inv_df)

col1, col2 = st.columns(2)
col11,col12 = col1.columns(2)

col11.header("Filter Data Invoice")
in_inv = col11.text_input("Invoice No")

col12.header('Download Rekap')
col12.write("Hasil Filter dapat diunduh berikut:")
col12.download_button(
   "Download",
   st.session_state.inv_df[st.session_state.inv_df['Is Paid']].to_csv(index=False).encode('utf-8'),
   "rekap.csv",
   "text/csv",
   key='download-csv',
   type='primary'
)

if col11.button("Submit",type='primary'):
    if not in_inv:
        col11.error("Date is incomplete!")
    else:
        col11.success("Data is Submitted")
        col11.subheader("Summary:")
        col11.write("Company Name: " + st.session_state.inv_df[st.session_state.inv_df['Id Pelanggan'] == in_inv[:7]]['Company'].values[0])
        col11.write("Nominal (Rp): " + str(st.session_state.inv_df[st.session_state.inv_df['Id Pelanggan'] == in_inv[:7]]['Nominal (Rp)'].values[0]))
        col11.write("Payment Due Date: " + str(st.session_state.inv_df[st.session_state.inv_df['Id Pelanggan'] == in_inv[:7]]['Payment Due Date'].values[0]))
        col11.write("Is Paid: " + str(st.session_state.inv_df[st.session_state.inv_df['Id Pelanggan'] == in_inv[:7]]['Is Paid'].values[0]))

col2.header("Form Simulasi Pembayaran")
col2.write("Form dibawah adalah simulasi pembayaran melalui VA oleh Pengguna dan didapatkan respon dari service layanan pembayaran berupa nomor invoice")
pay_va = col2.text_input("Simulation No Invoice")
if col2.button("Pay",type='primary'):
    if not pay_va:
        col2.error("Data is Incomplete!")
    else:
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