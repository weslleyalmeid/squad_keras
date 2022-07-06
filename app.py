import streamlit as st
import streamlit.components.v1 as components
import os.path
import pandas as pd
import numpy as np
import time
import plotly.express as px

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(ROOT_DIR, 'models')
DATA_DIR = os.path.join(ROOT_DIR, 'data', '{folder}')
data_file = os.path.join(DATA_DIR.format(folder='external'), 'creditcard.csv')
df = pd.read_csv(data_file)
df.columns = df.columns.str.lower()
model = pd.read_pickle( os.path.join(MODELS_DIR, "model.pkl"))


# st.set_page_config(page_title="Example App", page_icon="🤖")
st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)

st.sidebar.markdown(
    """ 
        Detecção de fraude em transações de cartão de crédito.
    """
)

opt = st.sidebar.radio('Selecione um opção', options=['Predict Only Data', 'Predict List Data', 'Dashboard', 'Dashboard 2'])


if opt == 'Predict Only Data':
    number = st.number_input('Amount', min_value=0)
    st.write('The current number is ', number)


elif opt == 'Predict List Data':
    file = st.file_uploader('Faça o upload do arquivo', type=['csv', 'xlsx'])
    
    if file is not None:
        try:
            df = pd.read_csv(file, usecols=model['features'])
        except:
            df = pd.read_excel(file, usecols=model['features'])

        if st.checkbox('Informações do Dataset'):
            st.markdown('Info')
            aux = pd.DataFrame({'types': df.dtypes,
                                'percentual_faltante': df.isna().mean()})

            st.dataframe(aux.astype(str))
            st.markdown('Shape')
            st.write(df.shape)

        if st.checkbox('Describe'):
            st.markdown('Describe')
            st.write(df.describe())

        if st.checkbox('Gerar detecção'):
            st.text('Modelo Random Forest')
            df['class'] = model['model'].predict(df)

            col = df.pop('class')
            df.insert(0, col.name, col)

            st.dataframe(df)
    



elif opt == 'Dashboard':
    iframe = """
    <iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="800" height="450"
    src="https://www.figma.com/embed?embed_host=share&url=https%3A%2F%2Fwww.figma.com%2Ffile%2FYTexnkXcRx4R0FNFeDKeiV%2FMinicurso-Design-de-Dashboards-com-Figma---Sayuri-Valente-(Community)%3Fnode-id%3D0%253A1" allowfullscreen>
    </iframe>
    """
    st.markdown(iframe,unsafe_allow_html=True)


elif opt == 'Dashboard 2':

    job_filter = st.selectbox("Select the Job", pd.unique(df["class"]))

    placeholder = st.empty()

    for seconds in range(200):

        df["time_new"] = df["time"] * np.random.choice(range(1, 5))
        df["amount_new"] = df["amount"] * np.random.choice(range(1, 5))

        # creating KPIs
        avg_time = np.mean(df["time_new"])

        count_fraud_amount = int(
            df[(df["class"] == 1)]["amount"].count() + np.random.choice(range(1, 5))
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
                label="Fraud Count",
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