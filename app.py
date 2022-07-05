import streamlit as st
import streamlit.components.v1 as components
import os.path
import pandas as pd

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(ROOT_DIR, 'models')

model = pd.read_pickle( os.path.join(MODELS_DIR, "model.pkl"))


def predict_model(model, data):
    pass


st.set_page_config(page_title="Example App", page_icon="🤖")

st.sidebar.markdown(
    """ 
        Detecção de fraude em transações de cartão de crédito.
    """
)

opt = st.sidebar.radio('Selecione um opção', options=['Predict Only Data', 'Predict List Data', 'Dashboard'])


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