import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Hub Inside Sales | Papapá", layout="wide")

# --- DATABASE INTEGRADA ---
equipe = {
    "Ana Christina Rodrigues": "Analista Pleno - Key Accounts",
    "Pedro Henrique Born": "Analista Pleno",
    "Joao Paulo Ferreira Alves": "Analista Junior",
    "Thiago Martins Cabral": "Estagiário - Operação",
    "Bernardo Oliveira Dallegrave": "Estagiário - Operação"
}

produtos = [
    {"Linha": "Papinhas de Carne", "Validade": "12 meses", "Un/Cx": 12, "Gramas": "120g"},
    {"Linha": "Papinhas de Fruta", "Validade": "16 meses", "Un/Cx": 12, "Gramas": "100g"},
    {"Linha": "Yoguzinho", "Validade": "15 meses", "Un/Cx": 16, "Gramas": "100g"},
    {"Linha": "Dentição (Biscoito de Arroz)", "Validade": "15 meses", "Un/Cx": 12, "Gramas": "-"},
    {"Linha": "Biscotti", "Validade": "10 meses", "Un/Cx": 12, "Gramas": "60g"},
    {"Linha": "La Chef / Sopinhas", "Validade": "16 meses/12 meses", "Un/Cx": 6, "Gramas": "240g (2x120g)"},
    {"Linha": "Macarrão Infantil", "Validade": "14 meses", "Un/Cx": 12, "Gramas": "200g"},
    {"Linha": "Cereal Infantil", "Validade": "12 meses", "Un/Cx": 12, "Gramas": "170g"},
    {"Linha": "Palitinhos de Vegetais", "Validade": "9 meses", "Un/Cx": 16, "Gramas": "45g"},
]

# --- SIDEBAR ---
st.sidebar.image("https://papapa.com.br/wp-content/uploads/2021/06/logo-papapa.png", width=120)
st.sidebar.title("Navegação")
menu = st.sidebar.radio("Selecione a área:", 
    ["💰 Metas e Comissionamento", "📦 Catálogo e SKUs", "🚚 Logística e Recebimento", "📝 Templates de Atendimento"])

# --- MÓDULO 1: COMISSIONAMENTO (SEM SALÁRIOS) ---
if menu == "💰 Metas e Comissionamento":
    st.title("📊 Painel de Premiação Mensal")
    st.info("O cálculo abaixo refere-se ao percentual de bônus sobre o salário fixo individual.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Simulador de Performance")
        analista = st.selectbox("Analista:", list(equipe.keys()))
        atingimento = st.number_input("Atingimento da Meta Individual (%)", min_value=0.0, value=100.0, step=1.0)
        
        st.write("---")
        st.subheader("Campanhas de Aceleração")
        faturamento_time = st.number_input("Faturamento Global do Time (R$)", value=1000000.0)
        venceu_destaque = st.checkbox("Destaque em Linha Específica (Mês)")

    with col2:
        st.subheader("Resultado da Apuração")
        
        # Lógica de Bônus Fixo
        if atingimento >= 110:
            status_bonus = "30% de Bônus"
            cor_metric = "normal"
        elif atingimento >= 90:
            status_bonus = "20% de Bônus"
            cor_metric = "normal"
        else:
            status_bonus = "Sem bonificação"
            cor_metric = "inverse"

        # Lógica de Aceleração
        extra_fat = 0
        if faturamento_time >= 1200000: extra_fat = 300
        elif faturamento_time >= 1000000: extra_fat = 100
        
        extra_destaque = 200 if venceu_destaque else 0

        st.metric("Status Bônus Fixo", status_bonus, delta=f"{atingimento}% da meta", delta_color=cor_metric)
        
        st.write("**Bônus Adicionais em Dinheiro:**")
        c1, c2 = st.columns(2)
        c1.metric("Aceleração Global", f"R$ {extra_fat},00")
        c2.metric("Prêmio Destaque", f"R$ {extra_destaque},00")
        
        st.success(f"**Total Extra em Dinheiro:** R$ {extra_fat + extra_destaque},00 + {status_bonus} sobre o salário.")

# --- MÓDULO 2: CATÁLOGO E SKUS ---
elif menu == "📦 Catálogo e SKUs":
    st.title("📋 Portfólio de Produtos Papapá")
    st.write("Consulte as informações técnicas para montagem de pedidos.")
    
    search = st.text_input("Filtrar linha de produto:")
    df_prod = pd.DataFrame(produtos)
    
    if search:
        df_prod = df_prod[df_prod['Linha'].str.contains(search, case=False)]
    
    st.table(df_prod)
    st.info("💡 Lembrete: Nossos produtos não precisam de refrigeração.")

# --- MÓDULO 3:
