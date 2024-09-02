import os
import streamlit as st
import json
from langflow.load import run_flow_from_json
import nest_asyncio
from dotenv import load_dotenv

# Aplicando nest_asyncio para permitir loops assíncronos aninhados
nest_asyncio.apply()

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
ft_key = os.getenv("OPENAI_FT_KEY")

if api_key is None:
    raise ValueError("A chave da API da OpenAI não foi encontrada. Defina a variável de ambiente OPENAI_API_KEY.")

if ft_key is None:
    raise ValueError("A chave do modelo fine-tuned da OpenAI não foi encontrada. Defina a variável de ambiente OPENAI_FT_KEY.")

os.environ["OPENAI_API_KEY"] = api_key
os.environ["OPENAI_FT_KEY"] = ft_key

def run_flow(tenant_id, client_id, client_secret, user_email) -> str:
    # Ajustes para o fluxo
    TWEAKS = {
        "FineTunedOpenAIModel-n4uK0": {"model_id": ft_key},  # Usando a chave fine-tuned do .env
        "ChatOutput-94COA": {},
        "ParseData-8zaoB": {},
        "Prompt-pe6IA": {},
        "CustomComponent-xnogf": {
            "tenant_id": tenant_id,
            "client_id": client_id,
            "client_secret": client_secret,
            "user_email": user_email
        }
    }
    
    # Defina o caminho absoluto do arquivo JSON atualizado
    flow_file_path = os.path.abspath("flow/lgpd_outlook_email.json")
    
    try:
        result = run_flow_from_json(
            flow=flow_file_path,
            input_value="",  # Deixando vazio pois o arquivo anexado será usado
            fallback_to_env_vars=True,
            tweaks=TWEAKS
        )

        # Processar a resposta do modelo
        if isinstance(result, list) and len(result) > 0:
            run_outputs = result[0]
            outputs = run_outputs.outputs
            if isinstance(outputs, list) and len(outputs) > 0:
                result_data = outputs[0].results
                if "message" in result_data and hasattr(result_data["message"], "data"):
                    message_data = result_data["message"].data.get("text", "Texto não encontrado.")
                    return message_data
                else:
                    return "Campo 'text' não encontrado em 'data'."
            else:
                return "Estrutura de 'outputs' inesperada."
        else:
            return "O fluxo não retornou nenhum resultado."

    except Exception as e:
        return f"Erro ao executar o fluxo: {str(e)}"

def trek_email():
    """Função principal para a página de análise de email"""
    create_header()
    create_chatbot()

# Função para criar o cabeçalho
def create_header():
    st.markdown(
        """
        <style>
        .header-text {
            background-color: #0464ac;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            color: #FFFFFF;
            margin-bottom: 20px;
        }
        .chatbot-box {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            border-left: 4px solid #2986c4;
            position: relative;
        }
        .response-box {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            border-left: 4px solid #47c2ec;
            position: relative;
        }   
        .stButton>button {
            background-color: #5687bf;
            color: white;
            border-radius: 8px;
            height: 50px;
            width: 100%;
            font-size: 16px;
        }
        </style>
        """, unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div class="header-text">
            <h1 style="color: white;">LucIA</h1>
            <p>Olá, meu nome é LucIA, sou uma assistente de IA criada pela TrekIO.<br>Sou especialista em conformidade com a Lei Geral de Proteção de Dados (LGPD). Como posso te ajudar hoje?</p>
        </div>
        """, unsafe_allow_html=True
    )

# Função para criar a interface do chatbot
def create_chatbot():
    st.markdown("<div class='chatbot-box'><h2>Insira as credenciais para análise</h2></div>", unsafe_allow_html=True)

    # Input de credenciais
    tenant_id = st.text_input("Tenant ID", "")
    client_id = st.text_input("Client ID", "")
    client_secret = st.text_input("Client Secret", type="password")
    user_email = st.text_input("User Email", "")

    # Botão para iniciar a análise
    if st.button("Analisar"):
        if tenant_id and client_id and client_secret and user_email:
            response = run_flow(tenant_id, client_id, client_secret, user_email)
            st.markdown(f"<div class='response-box'><h3>Resposta</h3><p>{response}</p></div>", unsafe_allow_html=True)

            # Botão para reiniciar a página
            if st.button("Nova Consulta"):
                st.experimental_rerun()
        else:
            st.warning("Por favor, preencha todas as credenciais.")

# Função principal
def main():
    create_header()
    create_chatbot()

if __name__ == "__main__":
    main()
