import os.path
import time
from datetime import datetime, date

import ipdb
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.utils import Utils

ut = Utils()

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
    number = st.number_input('Page number', min_value=1, max_value=2)
    if number == 1:
        st.title('Detecção de fraudes em cartões de crédito')
        st.subheader('Engenharia de Dados')
        st.write('[Bianca de Moura Pasetto](https://www.linkedin.com/in/biancamk)')
        st.write('[Enzo  Niro]()')

        st.subheader('Ciência de Dados')
        st.write('[Marco Craveiro](https://www.linkedin.com/in/marco-craveiro-ab577310)')
        st.markdown('[Weslley Almeida](https://www.linkedin.com/in/weslleyalmeid)')
        

    elif number == 2:
        st.write('### [Repo github](https://github.com/weslleyalmeid/squad_keras)')
        st.write('### [Apresentação](https://docs.google.com/presentation/d/19ZaNbDVx2X4GQsaP2_BChKiQ6bpxSTDV/edit?usp=sharing&ouid=100868357269049707274&rtpof=true&sd=true)')



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
                    # 'uri': 'http://172.18.0.2:5000/',
                    'uri': "https://keras-fraud-detection.herokuapp.com/",
                    'name_registry': 'model_clf',
                    'name_experiment': 'fraud_detection'
                }

                model, features, name, importance = ut.get_model(text=option.lower(), params=params)
           
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

                df['model'] = name

                dt = datetime.today().date()
                df['dt_arquivo'] = dt

                st.download_button(
                    label='Download Result',
                    data=df.to_csv(index=False).encode('utf-8'),
                    file_name=f'result_{dt}.csv',
                    mime='text/csv"',
                    key='download-csv'
                )

                kpi1, kpi2 = st.columns(2)

                count_fraud = df.loc[df['class'] == 1].shape[0]
                count_normal = df.loc[df['class'] == 0].shape[0]
                total_operations = df.shape[0]

                kpi1.metric(
                    label="Quantidade de operações",
                    value=total_operations
                )

                kpi1.metric(
                    label="Quantidade de operações normais",
                    value=count_normal
                )

                kpi2.metric(
                    label="Quantidade de fraude",
                    value=count_fraud
                )
                
                kpi2.metric(
                    label="% de operações fraudulentas",
                    value=f'{round(100*(count_fraud/total_operations), 2)}%'
                )
                
                col3, col4 = st.columns([3, 1])
                with col3:
                    st.dataframe(df)
                with col4:
                    st.code(importance)

                ut.save_db(df)


    

elif opt == 'KPIs':

    st.title('Métricas de Monitoramento')

    st.markdown('Selecione um intervalo:')
    col1, col2 = st.columns(2)

    df = ut.get_data_predict()
    all_date = pd.unique(df['dt_arquivo'].sort_values())
    
    
    with col1:
        dt_min = st.selectbox(label='Data inferior', options=all_date, index=0)

    with col2: 
        dt_max = st.selectbox(label='Data superior', options=all_date, index=len(all_date)-1)


    placeholder = st.empty()

    money_total = df['amount'].sum()
    money_fraud = df.loc[df['class'] == 1, 'amount'].sum()
    money_normal = df.loc[df['class'] == 0, 'amount'].sum()

    count_fraud = df.loc[df['class'] == 1].shape[0]
    count_normal = df.loc[df['class'] == 0].shape[0]
    total_operations = df.shape[0]

    # creating KPIs
    job_filter = 1
    count_fraud_amount = df[(df["class"] == job_filter)]["amount"].count()


    with placeholder.container():

        # create three columns
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        # fill in those three columns with respective metrics or KPIs
        kpi1.metric(
            label="R$ fraude detectada",
            value=f"R$ {round(money_fraud,2)}".replace('.', ',')
        )
        
        kpi2.metric(
            label="R$ operação normal",
            value=f"R$ {round(money_normal,2)}".replace('.', ',')
        )
        
        kpi3.metric(
            label="R$ Total avaliado",
            value=f"R$ {round(money_total,2)}".replace('.', ',')
        )

        kpi4.metric(
            label="Faturamento para 0.5%",
            value=f"R$ {round(money_total*0.05,2)}".replace('.', ',')
        )

        kpi5, kpi6, kpi7, kpi8 = st.columns(4)

        kpi5.metric(
            label="% de fraude em R$",
            value=f'{round(100*(money_fraud/money_total), 2)}%'
        )

        kpi6.metric(
            label="Quantidade de operações",
            value=total_operations
        )

        kpi7.metric(
            label="Quantidade de fraude",
            value=count_fraud
        )
        
        kpi8.metric(
            label="% de operações fraudulentas",
            value=f'{round(100*(count_fraud/total_operations), 2)}%'
        )
        
        fig_col1, fig_col2 = st.columns([3, 1])

        with fig_col1:
            df_tmp = df.groupby(['dt_arquivo', 'class']).agg({'amount':'sum'}).reset_index()
            fig = px.bar(
                data_frame=df_tmp,
                x='dt_arquivo',
                y='amount',
                color='class',
                hover_data={'dt_arquivo':'dd-mm-yyyy'},
                title="Valores de operações diárias",
                labels={
                     "dt_arquivo": "Data",
                     "amount": "Valor em Reais"
                 },
                )
            fig.update_xaxes(rangeslider_visible=True)
            fig.update_layout(
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with fig_col2:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = count_fraud,
                delta = {'reference': 500, 'increasing': {'color': "red"}},
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Fraudes"}))
            st.markdown("Second Chart")
            st.plotly_chart(fig, use_container_width=True)


        st.subheader('Informações da bases de operações')
        st.dataframe(df)


elif opt == 'Dashboard':
    iframe = """
    <iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="800" height="450"
    src="https://www.figma.com/embed?
    embed_host=share&url=https%3A%2F%2Fwww.figma.com%2Fproto%
    2FjeOMQxGGahuGYbqARVNifB%2Fexample_dash%3Fnode-id%3D4%253A369%2
    6scaling%3Dmin-zoom%26page-id%3D0%253A1" allowfullscreen></iframe>
    """
    st.markdown(iframe,unsafe_allow_html=True)


