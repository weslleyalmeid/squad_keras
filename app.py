import streamlit as st
import streamlit.components.v1 as components
import os.path
import pandas as pd
import numpy as np
import time
import plotly.express as px
import ipdb
import mlflow
from src.utils import Utils

ut = Utils()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data', '{folder}')
data_file = os.path.join(DATA_DIR.format(folder='external'), 'creditcard.csv')
df = pd.read_csv(data_file)
df.columns = df.columns.str.lower()

st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="🤖",
    layout="wide",
)

st.sidebar.markdown(
    """ 
        Detecção de fraude em transações de cartão de crédito.
    """
)

option = ['Sobre', 'Predict List Data', 'KPIs', 'Dashboard']
opt = st.sidebar.radio('Selecione um opção', options=option)


if opt == 'Sobre':
    number = st.number_input('Page number', min_value=1, max_value=3)
    if number == 1:
        st.write('The current number is ', number)
    elif number == 2:
        st.write('The current number is ', number)
    elif number == 3:
        st.write('The current number is ', number)


elif opt == 'Predict List Data':
    file = st.file_uploader('Faça o upload do arquivo', type=['csv', 'xlsx'])
    
    if file is not None:
        df = ut.read_file(file)

        if st.checkbox('Informações dos Dados'):

            col1, col2 = st.columns(2)

            with col1:
                st.markdown('Informações')
                aux = pd.DataFrame({'types': df.dtypes,
                                    'percentual_faltante': df.isna().mean()})

                st.write(aux.astype(str))
                st.markdown('Detalhes')
                st.write(f'A base de dados tem {df.shape[0]} elementos e {df.shape[1]} colunas')

            with col2:
                st.markdown('Descritivos')
                st.write(df.describe())

        if st.checkbox('Gerar detecção'):
            option = st.selectbox(
            'Selecione o Modelo?',
            ('Nenhum', 'Random Forest Local', 'Random Forest MLFlow'))

            if option != 'Nenhum':
                params = {
                    'uri': 'http://0.0.0.0:5000',
                    'name_registry': 'model_clf',
                    'name_experiment': 'fraud_detection'
                }

                model, features, name = ut.get_model(text=option.lower(), params=params)

                st.write(f'Modelo: {name}')
                y_pred = model.predict(df[features])
                y_pred_proba = model.predict_proba(df[features])

                df['class'] = y_pred
                df[['class_percent_0', 'class_percent_1']] = y_pred_proba

                col = df.pop('class_percent_0')
                df.insert(0, col.name, col)

                col = df.pop('class_percent_1')
                df.insert(0, col.name, col)

                col = df.pop('class')
                df.insert(0, col.name, col)

                st.dataframe(df)

                st.download_button(
                    label='Download Result',
                    data=df.to_csv(index=False).encode('utf-8'),
                    file_name='result.csv',
                    mime='text/csv"',
                    key='download-csv'
                )

    

elif opt == 'KPIs':

    job_filter = st.selectbox("Select the Job", pd.unique(df["class"]))

    placeholder = st.empty()

    for seconds in range(10000):

        df["time_new"] = df["time"] * np.random.choice(range(1, 5))
        df["amount_new"] = df["amount"] * np.random.choice(range(1, 5))

        # creating KPIs
        avg_time = np.mean(df["time_new"])

        count_fraud_amount = int(
            df[(df["class"] == job_filter)]["amount"].count() + np.random.choice(range(1, 5))
        )

        balance = np.mean(df["amount_new"])

        with placeholder.container():

            # create three columns
            kpi1, kpi2, kpi3 = st.columns(3)

            # fill in those three columns with respective metrics or KPIs
            kpi1.metric(
                label="Age ⏳",
                value=round(avg_time),
                delta=round(avg_time) - 10,
            )
            
            kpi2.metric(
                label="{act} Count".format(act = 'Fraud' if job_filter == 1 else 'Normal'),
                value=int(count_fraud_amount),
                delta=-10 + count_fraud_amount,
            )
            
            kpi3.metric(
                label="A/C Balance ＄",
                value=f"$ {round(balance,2)} ",
                delta=-round(balance / count_fraud_amount) * 100,
            )

            # create two columns for charts
            fig_col1, fig_col2 = st.columns(2)
            with fig_col1:
                st.markdown("### First Chart")
                fig = px.density_heatmap(data_frame=df, y="time_new", x="amount_new", width=500, height=300)
                st.write(fig)
                
            with fig_col2:
                st.markdown("### Second Chart")
                fig2 = px.histogram(data_frame=df, x="amount_new", width=500, height=300)
                st.write(fig2)

            st.markdown("### Detailed Data View")
            st.dataframe(df)
            time.sleep(1)


elif opt == 'Dashboard':
    iframe = """
    <iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="800" height="450"
    src="https://www.figma.com/embed?
    embed_host=share&url=https%3A%2F%2Fwww.figma.com%2Fproto%
    2FjeOMQxGGahuGYbqARVNifB%2Fexample_dash%3Fnode-id%3D4%253A369%2
    6scaling%3Dmin-zoom%26page-id%3D0%253A1" allowfullscreen></iframe>
    """
    st.markdown(iframe,unsafe_allow_html=True)


