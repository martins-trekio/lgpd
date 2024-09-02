import os
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Importação das páginas
from pages.Home import home
from pages.TrekEmail import trek_email
from pages.TrekFile import trek_file

# Carregar configuração do arquivo config.yaml
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Configurar autenticação
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')
    st.sidebar.title("Navegação")
    paginas = st.sidebar.selectbox("Selecione uma página", ["Home", "Análise de Email", "Análise de Arquivo"])

    if paginas == "Home":
        home()
    elif paginas == "Análise de Email":
        trek_email()
    elif paginas == "Análise de Arquivo":
        trek_file()

elif st.session_state["authentication_status"] is False:
    st.error("Usuário/Senha inválido")
elif st.session_state["authentication_status"] is None:
    st.warning("Por Favor, utilize seu usuário e senha!")
