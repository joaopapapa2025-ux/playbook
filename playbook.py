import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Dashboard Inside Sales | Papapá", layout="wide")

# --- BANCO DE DADOS INTERNO (EXTRAÍDO DOS SEUS DOCUMENTOS) ---
produtos_lista = [
    {"Linha": "Papinhas de Carne", "Validade": "12 meses", "Un/Cx": 12, "Peso": "120g", "Sabores": "Carne, Arroz e Legumes / Frango, Mandioquinha e Legumes"},
    {"Linha": "Yoguzinho", "Validade": "15 meses", "Un/Cx": 16, "Peso": "100g", "Sabores": "Maçã e Banana / Morango e Banana"},
    {"Linha": "Papinhas de Fruta", "Validade": "16 meses", "Un/Cx": 12, "Peso": "100g", "Sabores": "Maçã, Manga, Pêra, Ameixa, Banana"},
    {"Linha": "Dentição (Biscoito Arroz)", "Validade": "15 meses", "Un/Cx": 12, "Peso": "30g", "Sabores": "Maçã e Canela / Morango e Banana"},
    {"Linha": "Biscotti", "Validade": "10 meses", "Un/Cx": 12, "Peso": "60g", "Sabores": "Maçã / Banana"},
    {"Linha": "La Chef", "Validade": "16 meses", "Un/Cx": 6, "Peso": "240g", "Sabores": "Risotinho de Carne / Galinhada"},
    {"Linha": "Sopinhas", "Validade": "12 meses", "Un/Cx": 6, "Peso": "240g", "Sabores": "Feijão, Carne e Legumes / Canja de Galinha"},
    {"Linha": "Macarrão", "Validade": "14 meses", "Un/Cx": 12, "Peso": "200g", "Sabores": "Letrinhas / Estrelinhas"},
    {"Linha": "Cereal Infantil", "Validade": "12 meses", "Un/Cx": 12, "Peso": "170g", "Sabores": "Multicereais / Aveia e Morango"},
    {"Linha": "Palitinhos", "Validade": "9 meses", "Un/Cx": 16, "Peso": "45g", "Sabores": "Milho / Cenoura"},
]

# 2. SIDEBAR
st.sidebar.image("https://papapa.com.br/wp-content/uploads/2021/06/logo-papapa.png", width=120)
menu = st.sidebar.radio("Navegação:", ["💰 Comissão", "📦 Produtos", "🚚 Logística", "📝 Templates"])

# --- MÓDULO 1: COMISSÃO ---
if menu == "💰 Comissão":
    st.title("📊 Calculadora de Premiação (Modelo 2026)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Simulador de Meta")
        atingimento = st.number_input("Atingimento Individual (%)", min_value=0.0, value=100.0)
        fat_global = st.number_input("Faturamento Global Time (R$)", value=1000000.0)
        destaque = st.checkbox("Ganhou prêmio de destaque?")
        
    with col2:
        st.subheader("Resultado do Bônus")
        if atingimento >= 110:
            status = "30% de Bônus"
        elif atingimento >= 90:
            status = "20% de Bônus"
        else:
            status = "0% (Abaixo de 90%)"
            
        st.metric("Bônus sobre Salário", status)
        
        # Aceleração Cash
        acel = 300 if fat_global >= 1200000 else (100 if fat_global >= 1000000 else 0)
        premio = 200 if destaque else 0
        
        st.write(f"**+ Adicional em Dinheiro:** R$ {acel + premio},00")

# --- MÓDULO 2: PRODUTOS ---
elif menu == "📦 Produtos":
    st.title("📦 Tabela Técnica de SKUs")
    st.dataframe(pd.DataFrame(produtos_lista), use_container_width=True, hide_index=True)
    st.info("💡 Todos os itens são Shelf Life (não precisam de geladeira).")

# --- MÓDULO 3: LOGÍSTICA (PREENCHIDO) ---
elif menu == "🚚 Logística":
    st.title("🚚 Protocolo de Recebimento e Logística")
    
    st.error("⚠️ REGRA OURO: SEM RESSALVA NA NF = SEM REPOSIÇÃO")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        ### Fluxo de Prazos
        1. **Separação:** 3 dias úteis.
        2. **Faturamento:** +2 dias úteis.
        3. **Coleta:** Após o 5º dia útil.
        *Frete CIF para todo o Brasil.*
        """)
    with col_b:
        st.markdown("""
        ### Como agir na Avaria:
        - Conferir antes de liberar o motorista.
        - Escrever o problema no verso da NF.
        - Se for parcial: Aceita o bom e emite **NFD** do ruim.
        - Se for total: Recusa a carga inteira.
        """)

# --- MÓDULO 4: TEMPLATES (PREENCHIDO) ---
elif menu == "📝 Templates":
    st.title("📝 Templates e Regras Financeiras")
    
    with st.expander("💳 Prazos de Boleto por Região"):
        st.markdown("**Sul e Sudeste:**")
        st.code("Até R$1k: 30d | R$1k-2k: 30/45d | > R$2k: 30/45/60d")
        st.markdown("**Norte, Nordeste, Centro-Oeste, MG e ES:**")
        st.code("Até R$1k: 45d | R$1k-2k: 45/60d | > R$2k: 40/50/60d")
        
    with st.expander("📧 Template: Resumo Comercial"):
        texto = """Olá! Seguem condições Papapá:
- Pedido Mínimo: R$ 800,00
- Frete: Grátis (CIF)
- Pagamento: Boleto ou PIX
- Validade: 12 a 16 meses"""
        st.text_area("Copiar:", value=texto, height=120)
        
    with st.expander("🔄 Trocas e Cadastro"):
        st.write("**Trocas:** Avisar com 60 dias de antecedência ao vencimento.")
        st.write("**Cadastro:** Enviar CNPJ, IE, E-mail e Telefone Financeiro para contasareceber2@papapa.com.br")
