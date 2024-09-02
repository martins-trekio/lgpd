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

def run_flow(file_path: str) -> str:
    # Ajustes para o fluxo
    TWEAKS = {
        "ChatOutput-94COA": {},
        "FineTunedOpenAIModel-n4uK0": {"model_id": ft_key},  # Usando a chave fine-tuned do .env
        "Prompt-uZYGB": {},
        "File-8EGIu": {"path": file_path},
        "ParseData-N4d7H": {},
    }
    
    # Defina o caminho absoluto do arquivo JSON atualizado
    flow_file_path = os.path.abspath("flow/lgpd_langflow_trekcob.json")
    
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

def trek_file():
    """Função principal para a página de análise de arquivos"""
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
            <p>Olá, meu nome é LucIA, sou uma assistente de IA criada pela TrekIO.<br>Sou especialista em conformidade com a Lei Geral de Proteção de Dados (LGPD).</p>
        <div class="header-text">
            <p> Anexe seu arquivo e confira se ele está de acordo com a LGPD.</p>
        </div>
        """, unsafe_allow_html=True
    )

# Função para criar a interface do chatbot
def create_chatbot():
    st.markdown("<div class='chatbot-box'><h2>Envie arquivos para análise</h2></div>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Escolha arquivos PDF ou Word", type=["pdf", "docx"], accept_multiple_files=True)
    
    if uploaded_files:
        if st.button("Analisar"):
            temp_dir = "tmp"
            os.makedirs(temp_dir, exist_ok=True)

            responses = []
            for uploaded_file in uploaded_files:
                temp_file_path = os.path.abspath(os.path.join(temp_dir, uploaded_file.name))
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                response = run_flow(temp_file_path)
                if response:
                    responses.append((uploaded_file.name, response))
                else:
                    responses.append((uploaded_file.name, "Erro ao processar o arquivo."))

            for file_name, response in responses:
                st.markdown(f"<div class='response-box'><h3>Resposta para {file_name}</h3><p>{response}</p></div>", unsafe_allow_html=True)
   
            # Botão para reiniciar a página
            if st.button("Nova Consulta"):
                st.experimental_rerun()
    else:
        st.warning("Por favor, anexe um ou mais arquivos para análise.")

# Função principal
def main():
    create_header()
    create_chatbot()

if __name__ == "__main__":
    main()
