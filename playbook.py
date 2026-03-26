import streamlit as st
import pandas as pd
import base64

# --- CONFIGURAÇÕES DE ESTILO ---
st.set_page_config(page_title="Papapá | Sales OS", layout="wide", page_icon="💙")

# CSS para identidade visual
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE SUPORTE ---
def download_link(file_path, label):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        return f'<a href="data:application/octet-stream;base64,{b64}" download="{file_path}" style="color: #007bff; font-weight: bold; text-decoration: none;">⬇️ {label}</a>'
    except FileNotFoundError:
        return f'<span style="color: red;">❌ Arquivo {file_path} não encontrado</span>'

# --- SIDEBAR NAVEGAÇÃO ---
st.sidebar.title("🚀 Papapá Sales OS")
aba = st.sidebar.radio("Navegação:", [
    "📊 Dashboard Performance", 
    "💰 Tabela de Preços", 
    "📄 Biblioteca de Arquivos", 
    "🚚 Logística e SAC",
    "✍️ Scripts de Vendas"
])

# --- 1. DASHBOARD DE PERFORMANCE ---
if aba == "📊 Dashboard Performance":
    st.title("📊 Performance Inside Sales")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pedido Mínimo", "R$ 800,00", "Fixo")
    c2.metric("Time Ativo", "5 Analistas", "Capacidade Máxima")
    c3.metric("Prazo Médio", "30/45/60", "Boleto")
    c4.metric("Frete", "CIF", "Brasil")

    st.divider()
    
    col_time, col_metas = st.columns([1, 2])
    
    with col_time:
        st.subheader("👥 Divisão do Time")
        st.info("""
        **Key Accounts:** Ana Christina & Pedro Born
        **Tier 1 & 2:** Joao Paulo
        **Reativação/Vekta:** Thiago & Bernardo
        """)
        
    with col_metas:
        st.subheader("🎯 Simulador de Comissionamento")
        meta_val = st.slider("Simular atingimento da meta (%)", 80, 120, 100)
        
        if meta_val >= 110:
            st.balloons()
            st.success(f"**Status:** Superação ({meta_val}%) | **Bônus:** 30% Salário + Acelerador")
        elif meta_val >= 100:
            st.success(f"**Status:** Meta Batida | **Bônus:** 25% Salário")
        elif meta_val >= 90:
            st.warning(f"**Status:** Piso de Entrega | **Bônus:** 20% Salário")
        else:
            st.error("**Status:** Abaixo do Piso. Foco total em Reativação!")

# --- 2. TABELA DE PREÇOS ---
elif aba == "💰 Tabela de Preços":
    st.title("💰 Consulta por Estado")
    
    nome_arquivo_precos = "Tabela de preços Papapá 0226 v2.xlsx - PREÇOS.csv"
    
    try:
        df = pd.read_csv(nome_arquivo_precos, skiprows=1)
        # Limpando nomes de colunas que podem vir com espaços
        df.columns = df.columns.str.strip()
        
        if 'Estado' in df.columns:
            estado_sel = st.selectbox("Selecione o Estado:", df['Estado'].unique())
            dados_busca = df[df['Estado'] == estado_sel].T
            dados_busca.columns = ["Preço Unitário (R$)"]
            st.table(dados_busca)
        else:
            st.warning("Coluna 'Estado' não encontrada no CSV.")
            st.write("Colunas detectadas:", list(df.columns))
    except Exception as e:
        st.error(f"Erro ao carregar a tabela: {e}")
        st.info("Certifique-se de que o arquivo CSV da tabela de preços está na mesma pasta do código.")

# --- 3. BIBLIOTECA DE ARQUIVOS ---
elif aba == "📄 Biblioteca de Arquivos":
    st.title("📄 Documentos e Catálogos")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("📁 Comercial")
        st.markdown(download_link("catalogo-papapa-digital.pdf", "Catálogo Digital 2026"), unsafe_allow_html=True)
        st.markdown(download_link("Informações todos os produtos Papapá.pdf", "Fichas Técnicas"), unsafe_allow_html=True)
        st.markdown(download_link("Estrutura de Operação e Metas - Inside Sales.pdf", "Manual de Metas"), unsafe_allow_html=True)

    with col_b:
        st.subheader("📁 Operacional")
        # CORREÇÃO DO ERRO DE SYNTAX: Linha única para evitar interrupção da string
        st.markdown(download_link("GUIA DE RECEBIMENTO DE MERCADORIAS.pdf", "Guia de Avarias"), unsafe_allow_html=True)
        st.markdown(download_link("Templates IS 2026.docx (2).pdf", "Playbook de Atendimento"), unsafe_allow_html=True)

# --- 4. LOGÍSTICA E SAC ---
elif aba == "🚚 Logística e SAC":
    st.title("🚚 Prazos e Ocorrências")
    
    st.warning("🚨 **REGRA DE OURO:** Ressalva na NF é obrigatória para qualquer avaria!")
    
    c1, c2 = st.columns(2)
    with c1:
        st.write("### Fluxo de Pedido")
        st.write("- **Separação:** Até 3 dias úteis")
        st.write("- **Faturamento:** Até 2 dias úteis")
        st.write("- **Coleta:** D+1 após faturamento")
    with c2:
        st.info("Dúvidas financeiras? Enviar e-mail para: **contasareceber2@papapa.com.br**")

# --- 5. SCRIPTS DE VENDAS ---
elif aba == "✍️ Scripts de Vendas":
    st.title("✍️ Templates de Mensagens")
    
    tema = st.selectbox("Tipo de contato:", ["Novo Cadastro", "Reativação", "Cobrança Amigável"])
    
    if tema == "Novo Cadastro":
        txt = "Olá! Para o cadastro na Papapá, preciso de: CNPJ, IE, E-mail Financeiro e Telefones de contato."
    elif tema == "Reativação":
        txt = "Sentimos sua falta! Temos novidades na linha de Papinhas e Frutas. Vamos repor seu estoque?"
    else:
        txt = "Identificamos um boleto pendente. Posso ajudar com a 2ª via ou comprovante?"

    st.text_area("Copie o texto abaixo:", value=txt, height=100)

# --- RODAPÉ ---
st.sidebar.divider()
st.sidebar.caption("v1.0.2 | Papapá Inside Sales 2026")
