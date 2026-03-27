import streamlit as st
import pandas as pd
import base64
from pathlib import Path

# --- CONFIGURAÇÕES DE ESTILO E PÁGINA ---
st.set_page_config(page_title="Papapá | Sales Hub", layout="wide", page_icon="💙")

# Função para carregar imagem e converter para base64 (necessário para HTML/CSS)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Configuração de imagem padrão (Papapa-azul..png)
# Certifique-se de que este arquivo está na mesma pasta que o script.
img_filename = "Papapa-azul..png"
if Path(img_filename).exists():
    img_base64 = get_base64_of_bin_file(img_filename)
    img_avatar_html = f"data:image/png;base64,{img_base64}"
else:
    # Imagem fallback caso o arquivo não seja encontrado (exemplo online)
    img_avatar_html = "https://www.w3schools.com/howto/img_avatar.png" 

# CSS Customizado para cards redondos (estilo LinkedIn) e Layout
st.markdown(f"""
    <style>
    /* Estilo da Página */
    .reportview-container {{
        background: #f0f2f6;
    }}
    
    /* Título Principal */
    h1 {{
        color: #004a99;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}

    /* Estilo do Card da Equipe */
    .team-card {{
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #eaeaea;
    }}
    
    /* Imagem Redonda (Estilo LinkedIn) */
    .avatar-round {{
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #007bff;
        margin-bottom: 15px;
    }}

    /* Nome Completo */
    .team-name {{
        font-weight: bold;
        font-size: 1.1em;
        color: #333;
        margin-bottom: 5px;
    }}

    /* Cargo */
    .team-role {{
        color: #666;
        font-size: 0.9em;
        margin-bottom: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- DADOS DA EQUIPE ---
equipe = [
    {
        "nome": "João Vitor Tadra",
        "cargo": "Coordenador",
        "foto_html": img_avatar_html
    },
    {
        "nome": "Ana Christina Rodrigues",
        "cargo": "Analista (Key Accounts)",
        "foto_html": img_avatar_html
    },
    {
        "nome": "Pedro Henrique Born",
        "cargo": "Analista (Crescimento)",
        "foto_html": img_avatar_html
    },
    {
        "nome": "Joao Paulo Ferreira Alves",
        "cargo": "Analista (Desenvolvimento)",
        "foto_html": img_avatar_html
    },
    {
        "nome": "Thiago Martins Cabral",
        "cargo": "Estagiário - Operação (Vekta/Reativação)",
        "foto_html": img_avatar_html
    },
    {
        "nome": "Bernardo Oliveira Dallegrave",
        "cargo": "Estagiário - Operação (Vekta/Reativação)",
        "foto_html": img_avatar_html
    }
]

# --- CABEÇALHO E NAVEGAÇÃO SUPERIOR ---
st.title("Hub Inside Sales | Papapá")
st.markdown("---")

# Menu de Navegação Superior
aba_selecionada = st.radio(
    "Navegação:",
    ["🏠 Home (Equipe)", "💰 Simulador de Bonificação", "📄 Biblioteca de Arquivos", "🚚 Logística & SAC", "✍️ Templates & Scripts", "🔗 Links Úteis"],
    horizontal=True
)

st.markdown("---")

# --- MÓDULO 1: HOME (VISUALIZAÇÃO DA EQUIPE) ---
if aba_selecionada == "🏠 Home (Equipe)":
    st.header("👥 Nossa Equipe")
    st.write("Conheça o time Inside Sales da Papapá.")
    
    # Criação de colunas para os cards (máximo 3 por linha)
    for i in range(0, len(equipe), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(equipe):
                membro = equipe[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="team-card">
                            <img src="{membro['foto_html']}" class="avatar-round" alt="{membro['nome']}">
                            <div class="team-name">{membro['nome']}</div>
                            <div class="team-role">{membro['cargo']}</div>
                        </div>
                    """, unsafe_allow_html=True)

# --- MÓDULO 2: SIMULADOR DE COMISSÃO (COM LÓGICA INTEGRADA) ---
elif aba_selecionada == "💰 Simulador de Bonificação":
    st.title("💰 Simulador de Comissionamento Individual")
    st.write("Calcule a projeção do seu bônus com base no atingimento da meta.")
    
    col_input, col_result = st.columns([1, 1.5])
    
    with col_input:
        st.subheader("Entrada de Dados")
        salario_base = st.number_input("Seu Salário Fixo Base (R$)", min_value=0.0, value=3000.0, step=100.0)
        meta_mes = st.number_input("Valor da Meta do Mês (R$)", min_value=0.0, value=150000.0, step=1000.0)
        resultado_atual = st.number_input("Seu Resultado Atual Batido (R$)", min_value=0.0, value=135000.0, step=1000.0)
        
    with col_result:
        st.subheader("Resultado")
        
        # Cálculo de Atingimento
        if meta_mes > 0:
            atingimento = (resultado_atual / meta_mes) * 100
        else:
            atingimento = 0.0
            
        # Lógica de Bonificação (Piso de 90%)
        # > 110% -> 30%
        # 90% a 109% -> 20%
        # < 90% -> 0%
        
        if atingimento >= 110.0:
            perc_bonus = 0.30
            cor_metric = "normal"
            status_meta = " Superação (110%+)!"
        elif atingimento >= 90.0:
            perc_bonus = 0.20
            cor_metric = "normal"
            status_meta = " Dentro do Piso (90-109%)"
        else:
            perc_bonus = 0.0
            cor_metric = "inverse" # Vermelho
            status_meta = " Abaixo do Piso (<90%)"
            
        valor_bonus = salario_base * perc_bonus
        total_estimado = salario_base + valor_bonus
        
        # Visualização de Métricas Coloridas
        st.metric(
            label="Atingimento da Meta",
            value=f"{atingimento:.1f}%",
            delta=status_meta,
            delta_color=cor_metric
        )
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric(
                label="Valor do Bônus",
                value=f"R$ {valor_bonus:,.2f}",
                delta=f"{perc_bonus*100:.0f}% sobre o fixo",
                delta_color=cor_metric
            )
        with c2:
            st.metric(
                label="Total (Fixo + Bônus)",
                value=f"R$ {total_estimado:,.2f}"
            )

import streamlit as st

# --- 1. CONFIGURAÇÕES DA PÁGINA (ESTILO E TÍTULO) ---
st.set_page_config(
    page_title="Papapá | Sales Hub 2026",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 2. CSS CUSTOMIZADO (Design Premium Papapá) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f7f9fc;
        color: #333333;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #eaeef2;
    }
    h1 {
        color: #004a99;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        margin-bottom: 20px;
    }
    h3 {
        color: #0056b3;
        font-size: 1.1em;
        font-weight: 600;
        margin-top: 15px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre;
        background-color: #ffffff;
        border-radius: 20px;
        border: 1px solid #eaeef2;
        color: #666666;
        padding: 0px 20px;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #eaeef2;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #007bff;
        color: #ffffff;
        font-weight: 600;
    }
    .stCode {
        background-color: #fcfcfc;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.03);
    }
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR E MENU DE NAVEGAÇÃO ---
st.sidebar.image("https://papapa.com.br/wp-content/uploads/2021/06/logo-papapa.png", width=140)
st.sidebar.title("Navegação Central")
st.sidebar.divider()

menu = st.sidebar.radio(
    "Selecione o Módulo:",
    ["✍️ Templates de Mensagens", "📊 Políticas e Prazos"]
)

# --- 4. MÓDULO: TEMPLATES DE MENSAGENS ---
if menu == "✍️ Templates de Mensagens":
    st.title("✍️ Hub de Templates & Scripts 2026")
    st.write("Abra a aba correspondente e clique no ícone de copiar rápida.")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🤝 Abordagem e Sondagem", 
        "🚀 Curva A & Mix Estratégico", 
        "📝 Cadastro e Pagamento", 
        "🚚 Logística e Prazos",
        "Pós-Venda e Trocas",
        "📂 Biblioteca de Arquivos"
    ])

    with tab1:
        st.write("### 📞 Primeiro Contato (Apresentação e Qualificação)")
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Modelos: Introdução e Sondagem Perfil**")
                with st.expander("Aproximação Cláss (Perfil Lojista)", expanded=True):
                    st.code("Olá, tudo bem?\nAqui é o [Seu Nome], da Papapá.\nVi que você se cadastrou na nossa página...", language=None)
                with st.expander("Abordagem Assertiva (Foco Negócio)", expanded=True):
                    st.code("Oi, tudo bem?\nSou o [Seu Nome], da Papapá.\nVi que você se cadastrou para receber mais informações...", language=None)
            with col2:
                st.write("**Modelos: Cadastro e Qualificação**")
                with st.expander("Abordagem Interessada (Catálogo)", expanded=True):
                    st.code("Oi, tudo bem?\nSou o [Seu Nome], da Papapá.\nQue legal ver seu interesse em trabalhar conosco!", language=None)
                with st.expander("Checklist de Qualificação Rápida", expanded=True):
                    st.code("• Que tipo de estabelecimento você tem?\n• Em qual cidade/bairro?\n• Seu público é mais família, fitness ou geral?", language=None)

    with tab2:
        st.write("### 🚀 Curva A: Giro e Recompra")
        st.info("Utilize este texto para educar o cliente sobre a nossa linha carro-chefe.")
        st.code("Hoje, a nossa Curva A é formada por:\n• Papinhas de fruta\n• Biscoitinho para fase da dentição\n• Biscotti", language=None)

    with tab3:
        st.write("### 📝 Cadastro e Dados Financeiros")
        col_cad, col_pix = st.columns(2)
        with col_cad:
            st.write("**1. Checklist de Documentação**")
            st.code("● CNPJ:\n● Inscrição Estadual (IE):\n● E-mail Financeiro:\n● E-mail Compras:", language=None)
        with col_pix:
            st.write("**2. Dados Oficiais para Pagamento**")
            st.code("Pix: CNPJ 34.282.307/0001-44\nItaú: Ag 8931 | CC 05510-0", language=None)

    with tab4:
        st.write("### 🚚 Logística e Condições")
        st.code("🔹 Pedido Mínimo: R$ 800,00.\n🔹 Frete: CIF (Grátis) para todo o Brasil.\n🔹 Prazo: 3 dias separação + 2 dias faturamento.", language=None)

    with tab5:
        st.write("### Pós-Venda e Ocorrências")
        st.warning("Sem a ressalva na Nota Fiscal, não conseguimos abrir ocorrência.")
        st.code("1. Registre a ressalva na NF.\n2. Não aceite os produtos avariados.\n3. Informe a Papapá imediatamente.", language=None)

    with tab6:
        st.write("### 📂 Biblioteca de Materiais")
        st.write("Baixe aqui os materiais atualizados para suporte às vendas.")
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Materiais de Venda**")
            st.button("📖 Baixar Catálogo Digital (PDF)")
            st.button("💰 Tabela de preços Papapá 0226 v2.xlsx")
        with c2:
            st.write("**Guias e Informações**")
            st.button("🎯 Estrutura de Operação e Metas")
            st.button("📋 GUIA DE RECEBIMENTO DE MERCADORIAS")

# --- 5. MÓDULO: POLÍTICAS E PRAZOS ---
if menu == "📊 Políticas e Prazos":
    st.title("📊 Políticas Comerciais Papapá 2026")
    col_valid, col_praz = st.columns(2)
    with col_valid:
        st.subheader("📅 Tabela de Validade (Shelf Life)")
        validade_dict = {"Papinhas Fruta": "16 meses", "Yoguzinho": "15 meses", "Dentição": "15 meses", "Biscotti": "10 meses"}
        st.table(validade_dict)
    with col_praz:
        st.subheader("💳 Prazos de Pagamento (Boleto)")
        st.write("**Sul e Sudeste:** 30d | 30/45d | 30/45/60d")
        st.write("**Outras Regiões:** 45d | 45/60d | 40/50/60d")
    
# --- MÓDULO 6: LINKS ÚTEIS ---
elif aba_selecionada == "🔗 Links Úteis":
    st.title("🔗 Central de Links Úteis")
    st.write("Acesse rapidamente as ferramentas e formulários da nossa operação.")
    
    # IMPORTANTE: Tudo abaixo daqui precisa estar indentado (com 4 espaços) para ficar dentro desta aba
    with st.container():
        st.subheader("📝 Cadastro e Operação")
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("📄 Forms Cadastro", "https://forms.office.com/pages/responsepage.aspx?id=KcXm9q-wZUOFUmPbM0a-aQ0xpHiomcxDhUissuWVgb9UMVU4UzNNWkc1REM3Vlk0SzVQMlZLSU5BWS4u&route=shorturl", use_container_width=True)
            st.caption("Novo cadastro e atualização de cadastro de clientes")
        with col2:
            st.link_button("👀 Acompanhar Cadastros", "https://papapacombr-my.sharepoint.com/:x:/g/personal/cadastros_papapa_com_br/IQDkMQgW0iAgTqw7aetudCfXAeVaoV7m17dbUSH7QNGzkv0?e=hQu864", use_container_width=True)
            st.caption("Acompanhamento da realização dos cadastros")

    st.markdown("---")

    with st.container():
        st.subheader("📊 Dashboards de Gestão")
        st.link_button("📈 Dashboard Clientes", "https://dashboard-clientes-swsbdiavx4hfqvjbtcvafs.streamlit.app/", use_container_width=True)
        st.info("**Senha:** amamosnossosclientes")

    st.markdown("---")

    st.subheader("🚚 Logística e Rastreamento")
    c1, c2 = st.columns(2)
    with c1:
        st.link_button("🚩 Solicitações Logísticas", "https://forms.office.com/Pages/ResponsePage.aspx?id=KcXm9q-wZUOFUmPbM0a-aQpGwsStRQZMoYBHJmx0xW1UMDhXRkQwSEQxU0cwUklNNVVGWTZFRUhVNS4u", use_container_width=True)
    with c2:
        st.link_button("📂 Respostas Solicitações", "https://papapacombr-my.sharepoint.com/:x:/g/personal/operacoes_papapa_com_br/IQDfqtRILiD4R5lmLjQujLN3AS4On6breUbk-qRT2a0sUYk?rtime=_eVdf_F13kg", use_container_width=True)
    
    st.link_button("📍 Follow-up de Entregas (Sharepoint)", "https://papapacombr.sharepoint.com/:x:/r/sites/Papapa-Fileserver/_layouts/15/Doc.aspx?sourcedoc=%7B5cf28a24-1caa-4578-8641-a96b089efffa%7D&action=edit", use_container_width=True)

    st.write("**Portais das Transportadoras:**")
    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown("**Translovato**")
        st.link_button("Rastrear Lovato", "https://www.translovato.com.br/portal/rastreamento")
        st.code("User: BABY\nPass: LOVATO")
    with t2:
        st.markdown("**Tecmar**")
        st.link_button("Portal Tecmar", "https://smonet.tecmartransportes.com.br/smonet/#/notas-fiscais")
        st.code("User: babyroo\nPass: babyroo1*")
    with t3:
        st.markdown("**Rodovitor**")
        st.link_button("Rastrear Rodovitor", "https://ssw.inf.br/2/rastreamento")
        st.caption("Acesso via SSW")

    st.markdown("---")

    with st.container():
        st.subheader("🎨 Marketing e Divulgação")
        col_m1, col_m2 = st.columns([1, 2])
        with col_m1:
            st.link_button("📂 Drive para Lojistas", "https://papapacombr-my.sharepoint.com/:f:/g/personal/bi_papapa_com_br/EkwEgijW7pNCm95ElhfbiHoBK4kVtHiWieDpIOmwFZwRgA", use_container_width=True)
        with col_m2:
            st.warning("**Senha de acesso:** Papapa@2023")
            st.write("Compartilhe com o cliente para fotos, logos e materiais de PDV.")
