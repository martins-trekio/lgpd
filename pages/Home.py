import streamlit as st

# Configuração da página com layout wide
st.set_page_config(
    page_title="Home - LucIA",
    page_icon="👩‍⚖️",
    layout="wide",  # Layout wide aplicado
)

def create_header():
    """Cria o cabeçalho da página"""
    
    st.markdown("""
        <style>
        .main {
            background-color: #FFFFFF;
        }
        .header-text {
            background-color: #0464ac;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            color: white;
            text-align: center;
        }
        .center-text {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
        }
        .feature-box {
            text-align: center;
            margin-top: -20px;
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 4px solid #2986c4;
        }
        .footer-box {
            text-align: justify;
            margin-top: 20px;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 10px;
            border-left: 4px solid #2986c4;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background-color:#0464ac;padding:20px;border-radius:15px;text-align:center;">
        <h1 style="color:white;">Bem-vindo à LucIA, sua especialista em LGPD</h1>
        <h2 style="color:white;">Proteja os dados da sua empresa com a LucIA</h2>
        <p style="font-size: 18px;color:white;">Conformidade, Análise e Segurança de Dados Pessoais</p>
    </div>
    """, unsafe_allow_html=True)
    
def create_main_features():
    """Cria a seção de funcionalidades principais"""
    st.write("### Funcionalidades Principais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
        """
        <div class="feature-box">
            <h3 style="color: #0464ac;">📧 Análise de E-mails</h3>
            <p>Analise a caixa de entrada de e-mails e verifique a conformidade com a LGPD.</p>
            <a href='/TrekEmail'>Acessar Análise de E-mails</a>
        </div>
        <div class="feature-box">
            <h3 style="color: #0464ac;">📄 Análise de Conformidade</h3>
            <p>Realize a análise detalhada dos dados para garantir conformidade com a LGPD.</p>
        </div>
        """, unsafe_allow_html=True
    )

    with col2:
        st.markdown(
        """
        <div class="feature-box">
            <h3 style="color: #0464ac;">📂 Análise de Arquivos</h3>
            <p>Anexe arquivos para análise de conformidade com a LGPD.</p>
            <a href='/TrekFile'>Acessar Análise de Arquivos</a>
        </div>
        <div class="feature-box">
            <h3 style="color: #0464ac;">🔔 Sua empresa em dia com a LGPD</h3>
            <p>LucIA garante a conformidade da sua empresa com a LGPD ao analisar e-mails e arquivos, identificando potenciais riscos e assegurando a proteção dos dados pessoais.</p>
        </div>
        """, unsafe_allow_html=True
    )

def create_footer():
    """Cria o rodapé da página"""
    st.markdown(
        """
        <div class="footer-box">
        <h4>Lucy IA: Sua aliada na conformidade com a LGPD</h4>
        <p>Lucy IA utiliza Inteligência Artificial para garantir que sua empresa esteja sempre em conformidade com as normas da LGPD, protegendo os dados pessoais e evitando riscos legais. Nossa solução é escalável, adaptável, e fácil de usar, proporcionando segurança e tranquilidade.</p>
        <p>Visite nosso site: <a href="https://www.trekio.com.br/" target="_blank">TrekIO</a></p>
        </div>
        """, unsafe_allow_html=True
    )

def home():
    """Página inicial do Sistema Lucy IA"""
    create_header()
    create_main_features()
    create_footer()

if __name__ == "__main__":
    home()
