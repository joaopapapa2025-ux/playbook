import streamlit as st
import pandas as pd
import base64

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Central Inside Sales | Papapá", layout="wide", page_icon="💙")

# --- FUNÇÃO PARA DOWNLOAD DE ARQUIVOS ---
def get_binary_file_downloader_html(bin_file, file_label='Arquivo'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{bin_file}" style="text-decoration: none; color: white; background-color: #007bff; padding: 8px 16px; border-radius: 5px;">📥 Baixar {file_label}</a>'
    return href

# 2. SIDEBAR E NAVEGAÇÃO
st.sidebar.image("https://papapa.com.br/wp-content/uploads/2021/06/logo-papapa.png", width=150)
st.sidebar.title("Menu de Navegação")
menu = st.sidebar.selectbox("Selecione a Área:", 
    ["🏠 Home", "📊 Metas e Operação", "💰 Calculadora de Comissão", "📦 Portfólio e Preços", "🚚 Logística e Recebimento", "📝 Templates de Atendimento"])

# --- ÁREA 1: HOME ---
if menu == "🏠 Home":
    st.title("Bem-vindo ao Portal Inside Sales 2026")
    st.markdown("""
    Esta central reúne todos os documentos oficiais da **Papapá**. 
    Use o menu lateral para navegar entre regras de negócio, tabelas de preços e materiais de apoio.
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Time:** 5 Analistas")
    with col2:
        st.success("**Meta Global:** Monitorada via RD CRM")
    with col3:
        st.warning("**Pedido Mínimo:** R$ 800,00")

# --- ÁREA 2: METAS E OPERAÇÃO ---
elif menu == "📊 Metas e Operação":
    st.title("📊 Estrutura de Operação e Metas")
    
    tab1, tab2 = st.tabs(["Divisão de Funções", "Arquivos Oficiais"])
    
    with tab1:
        st.markdown("""
        - **Analistas Plenos (Ana e Pedro):** Foco em Key Accounts (Tier VIP).
        - **Analista Júnior (João Paulo):** Foco em Contas Tier 1 e 2.
        - **Estagiários (Thiago e Bernardo):** Reativação, Pós-venda e Vekta.
        """)
        st.markdown(get_binary_file_downloader_html("Estrutura de Operação e Metas - Inside Sales.pdf", "Estrutura de Metas PDF"), unsafe_allow_html=True)

# --- ÁREA 3: COMISSÃO ---
elif menu == "💰 Calculadora de Comissão":
    st.title("💰 Simulador de Premiação")
    # Baseado no modelo de tiers de atingimento (90%, 100%, 110%)
    atingimento = st.slider("Atingimento da Meta Individual (%)", 0, 150, 100)
    
    if atingimento >= 110:
        bonus = "30% do Salário"
    elif atingimento >= 100:
        bonus = "25% do Salário"
    elif atingimento >= 90:
        bonus = "20% do Salário"
    else:
        bonus = "R$ 0,00 (Abaixo do piso)"
        
    st.metric("Estimativa de Bônus", bonus)
    st.caption("Campanhas de aceleração (Cash) são calculadas à parte conforme faturamento global.")

# --- ÁREA 4: PORTFÓLIO E PREÇOS ---
elif menu == "📦 Portfólio e Preços":
    st.title("📦 Tabela de Preços e Catálogo")
    
    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("Catálogo Digital")
        st.write("Consulte detalhes visuais e nutricionais.")
        st.markdown(get_binary_file_downloader_html("catalogo-papapa-digital.pdf", "Catálogo 2026"), unsafe_allow_html=True)
    
    with c2:
        st.subheader("Tabela de Preços")
        st.write("Tabela atualizada (Março 2026).")
        st.markdown(get_binary_file_downloader_html("Tabela de preços Papapá 0226 v2.xlsx - PREÇOS.csv", "Tabela de Preços (CSV)"), unsafe_allow_html=True)

    st.divider()
    st.subheader("Informações Técnicas por Linha")
    # Lendo o arquivo de informações de produtos
    st.markdown(get_binary_file_downloader_html("Informações todos os produtos Papapá.pdf", "Ficha Técnica Completa"), unsafe_allow_html=True)

# --- ÁREA 5: LOGÍSTICA ---
elif menu == "🚚 Logística e Recebimento":
    st.title("🚚 Protocolos Logísticos")
    
    col_log, col_img = st.columns([2, 1])
    
    with col_log:
        st.error("❗ REGRA OBRIGATÓRIA: Ressalva no verso da Nota Fiscal para qualquer avaria.")
        st.markdown("""
        **Prazos Operacionais:**
        - Separação: 3 dias úteis.
        - Faturamento: 2 dias úteis.
        - Coleta: Após o 5º dia útil.
        """)
        st.markdown(get_binary_file_downloader_html("GUIA DE RECEBIMENTO DE MERCADORIAS.pdf", "Guia de Avarias PDF"), unsafe_allow_html=True)
    
    with col_img:
        st.image("image_4f06e0.png", caption="Exemplo de Paletização/Produto", use_container_width=True)

# --- ÁREA 6: TEMPLATES ---
elif menu == "📝 Templates de Atendimento":
    st.title("📝 Templates IS 2026")
    
    st.info("Utilize os padrões abaixo para manter a comunicação 'Intermediária' (nem formal, nem informal demais).")
    
    with st.expander("💳 Prazos de Pagamento (Boleto)"):
        st.table({
            "Região": ["Sul/Sudeste", "Norte/NE/CO/MG/ES"],
            "Até R$ 1k": ["30 dias", "45 dias"],
            "R$ 1k - 2k": ["30/45 dias", "45/60 dias"],
            "Acima R$ 2k": ["30/45/60 dias", "40/50/60 dias"]
        })
        
    st.subheader("Resumo para WhatsApp/E-mail")
    template_venda = """Prezado [Nome], conforme conversamos, seguem as condições:
- Pedido Mínimo: R$ 800,00
- Frete: CIF (Grátis)
- Cadastro: Necessário CNPJ, IE e e-mail financeiro.
- Boletos: Enviados via e-mail automático."""
    st.text_area("Copiar Template:", value=template_venda, height=150)
    
    st.markdown(get_binary_file_downloader_html("Templates IS 2026.docx (2).pdf", "Templates Completos PDF"), unsafe_allow_html=True)

# --- RODAPÉ ---
st.sidebar.divider()
st.sidebar.caption("v2.1 | Atualizado em: Março 2026")
