import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Dashboard Inside Sales - Papapá", layout="wide")

# --- DADOS INTEGRADOS DOS DOCUMENTOS ---
equipe = {
    "Ana Christina Rodrigues": {"cargo": "Analista Pleno - Key Accounts", "salario": 5000.0, "meta": 400000.0},
    "Pedro Henrique Born": {"cargo": "Analista Pleno", "salario": 4000.0, "meta": 250000.0},
    "Joao Paulo Ferreira": {"cargo": "Analista Junior", "salario": 3000.0, "meta": 150000.0},
    "Thiago Martins Cabral": {"cargo": "Estagiário - Operação", "salario": 1500.0, "meta": 50000.0},
    "Bernardo Oliveira": {"cargo": "Estagiário - Operação", "salario": 1500.0, "meta": 50000.0}
}

produtos = [
    {"Linha": "Papinhas de Carne", "Validade": "12 meses", "Unidades/Cx": 12},
    {"Linha": "Yoguzinho", "Validade": "15 meses", "Unidades/Cx": 16},
    {"Linha": "Papinhas de Fruta", "Validade": "16 meses", "Unidades/Cx": 12},
    {"Linha": "Palitinhos", "Validade": "9 meses", "Unidades/Cx": 16},
    {"Linha": "Sopinhas/La Chef", "Validade": "12 meses", "Unidades/Cx": 6},
]

# --- SIDEBAR - NAVEGAÇÃO ---
st.sidebar.image("https://papapa.com.br/wp-content/uploads/2021/06/logo-papapa.png", width=150)
menu = st.sidebar.selectbox("Ir para:", ["Comissionamento & Metas", "Catálogo & Validades", "Logística & Avarias", "Templates de Venda"])

# --- MÓDULO 1: COMISSIONAMENTO & METAS ---
if menu == "Comissionamento & Metas":
    st.title("🚀 Performance e Comissionamento")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Simulador Individual")
        analista_ref = st.selectbox("Selecione o Analista", list(equipe.keys()))
        atingimento = st.slider("Atingimento da Meta (%)", 0, 150, 100)
        faturamento_total = st.number_input("Faturamento Global do Time (R$)", value=1100000.0)
        destaque_mes = st.checkbox("Ganhou 'Destaque de Linha'?")

    # Lógica de Cálculo (Baseada no Novo Modelo)
    salario_base = equipe[analista_ref]["salario"]
    bonus_percent = 0
    if atingimento >= 110:
        bonus_percent = 0.30
    elif atingimento >= 90:
        bonus_percent = 0.20
    
    comissao_fixa = salario_base * bonus_percent
    
    # Campanhas de Aceleração
    extra_faturamento = 0
    if faturamento_total >= 1200000:
        extra_faturamento = 300.0
    elif faturamento_total >= 1000000:
        extra_faturamento = 100.0
        
    extra_destaque = 200.0 if destaque_mes else 0.0
    total_receber = comissao_fixa + extra_faturamento + extra_destaque

    with col2:
        st.subheader(f"Resultado: {analista_ref}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Bónus Modelo Fixo", f"R$ {comissao_fixa:,.2f}")
        c2.metric("Campanha Faturamento", f"R$ {extra_faturamento:,.2f}")
        c3.metric("Bónus Destaque", f"R$ {extra_destaque:,.2f}")
        
        st.success(f"**Total de Premiação Estimada: R$ {total_receber:,.2f}**")
        st.info(f"Cargo: {equipe[analista_ref]['cargo']} | Salário Base: R$ {salario_base:,.2f}")

# --- MÓDULO 2: CATÁLOGO & VALIDADES ---
elif menu == "Catálogo & Validades":
    st.title("📦 Informações de Portfólio")
    st.write("Dados extraídos do Catálogo Digital e Tabela de Validades.")
    
    df_prod = pd.DataFrame(produtos)
    st.table(df_prod)
    
    st.warning("**Atenção:** Pedido mínimo para faturamento é de **R$ 800,00**.")

# --- MÓDULO 3: LOGÍSTICA & AVARIAS ---
elif menu == "Logística & Avarias":
    st.title("🚚 Guia de Recebimento e Prazos")
    
    tab1, tab2 = st.tabs(["Prazos de Pedido", "Protocolo de Avarias"])
    
    with tab1:
        st.markdown("""
        1. **Separação:** Até 3 dias úteis.
        2. **Faturamento:** + 2 dias úteis.
        3. **Coleta:** Após os 5 dias totais de processamento interno.
        """)
    
    with tab2:
        st.error("⚠️ REGRA OURO: Sem ressalva na NF, não há reposição!")
        st.markdown("""
        - **Conferência:** No ato da entrega.
        - **Divergência:** Registrar ressalva detalhada no verso da NF.
        - **Recusa Parcial:** Cliente aceita o que está ok e emite **NFD** (Nota de Devolução) do que está avariado.
        """)

# --- MÓDULO 4: TEMPLATES DE VENDA ---
elif menu == "Templates de Venda":
    st.title("📝 Templates Rápidos")
    
    st.subheader("Dados Necessários para Cadastro")
    cadastro_text = """CNPJ:
Inscrição Estadual (IE):
Telefone Financeiro/Compras:
E-mail Financeiro/Compras:
Dados Bancários (PIX):"""
    st.code(cadastro_text, language=None)
    
    st.subheader("Condições Comerciais (Frete CIF)")
    st.info("Utilize este texto para enviar propostas rápidas via WhatsApp ou E-mail.")
    st.text_area("Template:", value="Olá! Nossos produtos são vendidos em caixas fechadas. Frete CIF para todo o Brasil. Pedido mínimo R$ 800,00. Pagamento via Boleto ou PIX.", height=100)
