import streamlit as st
import streamlit.components.v1 as components

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


elif opt == 'Dashboard':
    iframe = """
    <iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="800" height="450"
    src="https://www.figma.com/embed?embed_host=share&url=https%3A%2F%2Fwww.figma.com%2Ffile%2FYTexnkXcRx4R0FNFeDKeiV%2FMinicurso-Design-de-Dashboards-com-Figma---Sayuri-Valente-(Community)%3Fnode-id%3D0%253A1" allowfullscreen>
    </iframe>
    """
    st.markdown(iframe,unsafe_allow_html=True)