import streamlit as st
import pandas as pd
import base64

# --- CONFIGURAÇÕES DE ESTILO ---
st.set_page_config(page_title="Papapá | Sales OS", layout="wide", page_icon="💙")

# CSS para deixar a cara da Papapá
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    .sidebar .sidebar-content { background-image: linear-gradient(#007bff, #0056b3); color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE SUPORTE ---
def download_link(file_path, label):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{file_path}" style="color: #007bff; font-weight: bold; text-decoration: none;">⬇️ {label}</a>'

# --- SIDEBAR NAVEGAÇÃO ---
st.sidebar.image("https://papapa.com.br/wp-content/uploads/2021/06/logo-papapa.png", width=150)
st.sidebar.title("Navegação")
aba = st.sidebar.radio("Ir para:", [
    "🚀 Dashboard Comercial", 
    "💰 Tabela de Preços Ativa", 
    "📄 Biblioteca de Arquivos", 
    "🚚 Logística e SAC",
    "✍️ Templates & Scripts"
])

# --- 1. DASHBOARD COMERCIAL (Visão Geral) ---
if aba == "🚀 Dashboard Comercial":
    st.title("🚀 Central de Performance Inside Sales")
    
    # Métricas de Cabeçalho
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pedido Mínimo", "R$ 800,00", "CIF")
    c2.metric("Time Ativo", "5 Analistas", "100%")
    c3.metric("Prazo Médio", "30/45/60", "Boleto")
    c4.metric("Status Operação", "Normal", "🔥")

    st.divider()
    
    col_time, col_metas = st.columns([1, 2])
    
    with col_time:
        st.subheader("👥 Equipe e Foco")
        st.info("**Ana & Pedro:** Key Accounts (VIP)\n\n**Joao Paulo:** Tier 1 e 2\n\n**Thiago & Bernardo:** Reativação e Vekta")
        
    with col_metas:
        st.subheader("🎯 Simulador de Atingimento")
        meta_val = st.slider("Simular % da Meta Alcançada", 80, 120, 100)
        if meta_val >= 110:
            st.balloons()
            st.success(f"**Status:** Superação (110%+) | **Premiação:** 30% Salário + Acelerador")
        elif meta_val >= 100:
            st.success(f"**Status:** Meta Batida | **Premiação:** 25% Salário")
        elif meta_val >= 90:
            st.warning(f"**Status:** Dentro do Piso | **Premiação:** 20% Salário")
        else:
            st.error("**Status:** Abaixo do esperado. Focar em Reativação!")

# --- 2. TABELA DE PREÇOS ATIVA ---
elif aba == "💰 Tabela de Preços Ativa":
    st.title("💰 Consulta de Preços por Estado")
    
    try:
        df_precos = pd.read_csv("Tabela de preços Papapá 0226 v2.xlsx - PREÇOS.csv", skiprows=1)
        estado = st.selectbox("Selecione o Estado do Cliente:", df_precos['Estado'].unique())
        
        dados_estado = df_precos[df_precos['Estado'] == estado].T
        dados_estado.columns = ["Valor Unitário (R$)"]
        
        st.dataframe(dados_estado.style.format(precision=2), use_container_width=True)
        st.caption("Valores sujeitos a alteração conforme tributação (ST) e regime tributário do cliente.")
    except:
        st.error("Erro ao ler a tabela de preços. Verifique se o arquivo CSV está no diretório.")

# --- 3. BIBLIOTECA DE ARQUIVOS ---
elif aba == "📄 Biblioteca de Arquivos":
    st.title("📄 Repositório de Documentos Oficiais")
    
    cols = st.columns(2)
    
    with cols[0]:
        st.write("### 📂 Materiais de Venda")
        st.markdown(download_link("catalogo-papapa-digital.pdf", "Catálogo Digital 2026"), unsafe_allow_html=True)
        st.markdown(download_link("Informações todos os produtos Papapá.pdf", "Fichas Técnicas e Nutricionais"), unsafe_allow_html=True)
        st.markdown(download_link("Estrutura de Operação e Metas - Inside Sales.pdf", "Regras de Metas e Cargos"), unsafe_allow_html=True)

    with cols[1]:
        st.write("### 📂 Operacional e Jurídico")
        st.markdown(download_link("GUIA DE RECE
