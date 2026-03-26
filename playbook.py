import streamlit as st
import pandas as pd

# Configurações iniciais
st.set_page_config(page_title="Papapá | Portal Inside Sales", layout="wide", initial_sidebar_state="expanded")

# --- BANCO DE DADOS INTEGRADO (EXTRAÍDO DOS DOCUMENTOS) ---
equipe_data = {
    "Ana Christina Rodrigues": {"cargo": "Analista Pleno - Key Accounts", "foco": "Grandes Contas (Tier VIP)", "metas": "Faturamento (~40% total), Expansão de Mix"},
    "Pedro Henrique Born": {"cargo": "Analista Pleno", "foco": "Ativação e Gestão de Carteira", "metas": "Faturamento de Ativação, Ticket Médio"},
    "Joao Paulo Ferreira Alves": {"cargo": "Analista Junior", "foco": "Suporte e Conversão da Base", "metas": "Conversão, Faturamento de Ativação"},
    "Thiago Martins Cabral": {"cargo": "Estagiário - Operação", "foco": "Reativação e Pós-Venda", "metas": "Receita de Reativação, Conversão Vekta, Churn"},
    "Bernardo Oliveira Dallegrave": {"cargo": "Estagiário - Operação", "foco": "Reativação e Pós-Venda", "metas": "Receita de Reativação, Conversão Vekta, Churn"}
}

produtos_data = [
    {"Linha": "Papinhas de Carne", "Validade": "12 meses", "Qtd/Cx": 12, "Destaque": "Ingredientes Naturais"},
    {"Linha": "Yoguzinho", "Validade": "15 meses", "Qtd/Cx": 16, "Destaque": "Sem refrigeração"},
    {"Linha": "Papinhas de Fruta", "Validade": "16 meses", "Qtd/Cx": 12, "Destaque": "Pouch prático"},
    {"Linha": "Dentição / Palitinhos", "Validade": "15 meses", "Qtd/Cx": 16, "Destaque": "Alimentação guiada"},
    {"Linha": "Biscotti", "Validade": "10 meses", "Qtd/Cx": 12, "Destaque": "Textura suave"},
    {"Linha": "La Chef / Sopinhas", "Validade": "16 meses", "Qtd/Cx": 6, "Destaque": "2 porções de 120g"},
    {"Linha": "Macarrão", "Validade": "14 meses", "Qtd/Cx": 12, "Destaque": "Cozimento rápido"},
    {"Linha": "Cereal Infantil", "Validade": "12 meses", "Qtd/Cx": 12, "Destaque": "Enriquecido com ferro"}
]

# --- SIDEBAR ---
st.sidebar.title("🛠️ Gestão Papapá")
aba = st.sidebar.radio("Selecione o Painel:", 
    ["📊 Performance & Bônus", "📦 Portfólio de Produtos", "🚚 Logística & Qualidade", "📝 Templates & Cadastro"])

st.sidebar.markdown("---")
st.sidebar.info("**Lembrete:** Pedido Mínimo R$ 800,00.")

# --- ABA 1: PERFORMANCE & BÔNUS (NOVO MODELO) ---
if aba == "📊 Performance & Bônus":
    st.title("🚀 Painel de Performance e Metas")
    
    col_sel, col_calc = st.columns([1, 2])
    
    with col_sel:
        st.subheader("Simulador Individual")
        nome = st.selectbox("Analista:", list(equipe_data.keys()))
        atingimento = st.number_input("Atingimento da Meta Individual (%)", min_value=0.0, max_value=200.0, value=100.0)
        salario = st.number_input("Salário Base (R$)", min_value=0.0, value=3000.0)
        
        st.write("---")
        st.subheader("Campanhas Globais")
        fat_global = st.number_input("Faturamento Mensal Time (R$)", value=1000000.0)
        destaque = st.checkbox("Destaque do Mês (Linha estratégica)")

    with col_calc:
        st.subheader(f"Projeção para: {nome}")
        st.caption(f"Foco: {equipe_data[nome]['foco']}")
        
        # Lógica de Comissionamento Fixa
        if atingimento < 90:
            perc_bonus = 0
            cor = "inverse"
        elif atingimento <= 109.9:
            perc_bonus = 0.20
            cor = "normal"
        else:
            perc_bonus = 0.30
            cor = "normal"
            
        valor_fixo = salario * perc_bonus
        
        # Campanhas de Aceleração
        bonus_global = 300.0 if fat_global >= 1200000 else (100.0 if fat_global >= 1000000 else 0)
        bonus_destaque = 200.0 if destaque else 0
        total = valor_fixo + bonus_global + bonus_destaque
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Bônus Fixo", f"R$ {valor_fixo:,.2f}", delta=f"{perc_bonus*100:.0f}%")
        c2.metric("Aceleração Global", f"R$ {bonus_global:,.2f}")
        c3.metric("Bônus Destaque", f"R$ {bonus_destaque:,.2f}")
        
        st.divider()
        st.subheader(f"Total Estimado: R$ {total:,.2f}")
        st.warning(f"**Métricas de Avaliação:** {equipe_data[nome]['metas']}")

# --- ABA 2: PORTFÓLIO DE PRODUTOS ---
elif aba == "📦 Portfólio de Produtos":
    st.title("📚 Catálogo e Especificações Técnicas")
    
    st.write("Consulte as validades e o padrão de encaxotamento para pedidos.")
    
    df_prod = pd.DataFrame(produtos_data)
    st.dataframe(df_prod, use_container_width=True, hide_index=True)
    
    st.info("💡 **Dica Comercial:** Todas as linhas dispensam refrigeração devido ao processo de envase.")

# --- ABA 3: LOGÍSTICA & QUALIDADE ---
elif aba == "🚚 Logística & Qualidade":
    st.title("🚛 Operação e Protocolo de Recebimento")
    
    col_log, col_ava = st.columns(2)
    
    with col_log:
        st.subheader("Prazos de Entrega (CIF)")
        st.markdown("""
        * **Separação:** 3 dias úteis (CD).
        * **Faturamento (NF):** +2 dias úteis.
        * **Coleta:** Após os 5 dias totais de processamento.
        * **Transporte:** Variável conforme região.
        """)
        
    with col_ava:
        st.subheader("⚠️ Regras de Avaria")
        st.error("**SEM RESSALVA = SEM REPOSIÇÃO**")
        st.markdown("""
        1. **Conferência:** Sempre no ato da entrega.
        2. **Ressalva:** Registrar no verso da NF qualquer dano visível.
        3. **Recusa Parcial:** Cliente aceita o que está bom e emite **NFD** (Nota de Devolução) do que está ruim.
        4. **Avaria Interna:** Não coberta se não houver ressalva na NF.
        """)

# --- ABA 4: TEMPLATES & CADASTRO ---
elif aba == "📝 Templates & Cadastro":
    st.title("📋 Suporte ao Fechamento")
    
    tab_cad, tab_temp = st.tabs(["Dados de Cadastro", "Templates de Texto"])
    
    with tab_cad:
        st.subheader("Informações Obrigatórias")
        st.code("""
CNPJ:
Inscrição Estadual (IE):
E-mail Financeiro/Compras:
Telefone Comercial:
Dados Bancários (Chave PIX):
        """, language=None)
        
    with tab_temp:
        st.subheader("Argumento Comercial Rápido")
        template = """Olá! Nossos produtos são naturais, sem conservantes e ideais para a introdução alimentar.
        - Pedido Mínimo: R$ 800,00
        - Frete: Grátis (CIF)
        - Pagamento: Boleto ou PIX
        - Validade média: 12 a 16 meses"""
        st.text_area("Copie o texto abaixo:", value=template, height=150)
