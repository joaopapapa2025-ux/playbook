import streamlit as st
import pandas as pd
import base64
from pathlib import Path

################################################################################
# --- 1. CONFIGURAÇÕES INICIAIS E ESTILO ---
################################################################################

st.set_page_config(
    page_title="Papapá | Sales Hub 2026",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Função para converter imagem em base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Tenta carregar o avatar da Papapá
img_filename = "Papapa-azul..png"
if Path(img_filename).exists():
    img_base64 = get_base64_of_bin_file(img_filename)
    img_avatar_html = f"data:image/png;base64,{img_base64}"
else:
    img_avatar_html = "https://www.w3schools.com/howto/img_avatar.png" 

# CSS Unificado
st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{display: none;}}
    div.row-widget.stRadio > div {{flex-direction: row; gap: 20px;}}
    .team-card {{
        background-color: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center;
        margin-bottom: 20px; border: 1px solid #eaeaea;
    }}
    .avatar-round {{
        width: 100px; height: 100px; border-radius: 50%;
        object-fit: cover; border: 3px solid #004a99; margin-bottom: 10px;
    }}
    .team-name {{ font-weight: bold; color: #333; }}
    .team-role {{ color: #666; font-size: 0.85em; }}
    .stCode {{ background-color: #fcfcfc; border-radius: 10px; border: 1px solid #e0e0e0; }}
    </style>
    """, unsafe_allow_html=True)

################################################################################
# --- 2. NAVEGAÇÃO PRINCIPAL ---
################################################################################

st.title("Hub Inside Sales | Papapá")

aba_selecionada = st.radio(
    "Navegação:",
    ["🏠 Home (Equipe)", "💰 Simulador de Bonificação", "📄 Biblioteca de Arquivos", "✍️ Templates & Scripts", "📊 Políticas & Prazos", "🔗 Links Úteis"],
    horizontal=True
)

st.divider()

################################################################################
# --- MÓDULO 1: HOME (EQUIPE) ---
################################################################################
if aba_selecionada == "🏠 Home (Equipe)":
    st.header("👥 Nossa Equipe")
    
    equipe = [
        {"nome": "João Vitor Tadra", "cargo": "Coordenador"},
        {"nome": "Ana Christina Rodrigues", "cargo": "Analista (Key Accounts)"},
        {"nome": "Pedro Henrique Born", "cargo": "Analista (Crescimento)"},
        {"nome": "Joao Paulo Ferreira Alves", "cargo": "Analista (Desenvolvimento)"},
        {"nome": "Thiago Martins Cabral", "cargo": "Estagiário - Operação"},
        {"nome": "Bernardo Oliveira Dallegrave", "cargo": "Estagiário - Operação"}
    ]
    
    for i in range(0, len(equipe), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(equipe):
                m = equipe[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="team-card">
                            <img src="{img_avatar_html}" class="avatar-round">
                            <div class="team-name">{m['nome']}</div>
                            <div class="team-role">{m['cargo']}</div>
                        </div>
                    """, unsafe_allow_html=True)

################################################################################
# --- MÓDULO 2: SIMULADOR DE BONIFICAÇÃO ---
################################################################################
elif aba_selecionada == "💰 Simulador de Bonificação":
    st.header("💰 Simulador de Comissionamento Individual")
    
    col_input, col_result = st.columns([1, 1.5])
    with col_input:
        salario_base = st.number_input("Salário Fixo (R$)", value=3000.0)
        meta_mes = st.number_input("Meta do Mês (R$)", value=150000.0)
        resultado_atual = st.number_input("Resultado Atual (R$)", value=135000.0)
        
    with col_result:
        atingimento = (resultado_atual / meta_mes) * 100 if meta_mes > 0 else 0.0
        if atingimento >= 110.0:
            perc, status, cor = 0.30, "Superação (110%+)", "normal"
        elif atingimento >= 90.0:
            perc, status, cor = 0.20, "No Piso (90-109%)", "normal"
        else:
            perc, status, cor = 0.0, "Abaixo do Piso", "inverse"
            
        valor_bonus = salario_base * perc
        st.metric("Atingimento", f"{atingimento:.1f}%", delta=status, delta_color=cor)
        st.metric("Bônus Estimado", f"R$ {valor_bonus:,.2f}", delta=f"{perc*100:.0f}%")

################################################################################
# --- MÓDULO 3: BIBLIOTECA DE ARQUIVOS ---
################################################################################
elif aba_selecionada == "📄 Biblioteca de Arquivos":
    st.header("📄 Biblioteca de Arquivos")
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📁 Materiais de Venda")
        arquivos = {
            "📖 Catálogo Digital": "catalogo-papapa-digital.pdf",
            "💰 Tabela de Preços": "Tabela de preços Papapá 0226 v2.xlsx",
            "ℹ️ Ficha Técnica": "Informações todos os produtos Papapá.pdf"
        }
        for label, path in arquivos.items():
            try:
                with open(path, "rb") as f:
                    st.download_button(label, f, file_name=path, use_container_width=True)
            except: st.error(f"Falta: {path}")

    with c2:
        st.subheader("📋 Guias e Processos")
        processos = {
            "🎯 Estrutura de Metas": "Estrutura de Operação e Metas - Inside Sales.pdf",
            "📦 Guia de Avarias": "GUIA DE RECEBIMENTO DE MERCADORIAS.pdf",
            "📝 Templates PDF": "Templates IS 2026.docx (2).pdf"
        }
        for label, path in processos.items():
            try:
                with open(path, "rb") as f:
                    st.download_button(label, f, file_name=path, use_container_width=True)
            except: st.error(f"Falta: {path}")

################################################################################
# --- MÓDULO 4: TEMPLATES & SCRIPTS ---
################################################################################
elif aba_selecionada == "✍️ Templates & Scripts":
    st.header("✍️ Templates & Scripts")
    t = st.tabs(["🤝 Abordagem", "🚀 Curva A", "📝 Cadastro", "🚚 Logística"])
    with t[0]:
        st.write("**Abordagem Perfil (WhatsApp)**")
        st.code("Olá, tudo bem? Aqui é o [Seu Nome], da Papapá...", language=None)
    with t[1]:
        st.write("**Sugestão Curva A** [cite: 242, 243]")
        st.code("Recomendamos iniciar com: Papinhas de Fruta, Biscoito Dentição e Biscotti.", language=None)

################################################################################
# --- MÓDULO 5: POLÍTICAS & PRAZOS ---
################################################################################
elif aba_selecionada == "📊 Políticas & Prazos":
    st.header("📊 Políticas Comerciais")
    st.info("**Pedido Mínimo:** R$ 800,00 [cite: 163]")
    st.write("**Prazos de Entrega:** 3 dias separação + 2 dias faturamento [cite: 175, 176]")
    st.write("**Validades:** Papinhas Fruta (16 meses), Yoguzinho (15 meses) [cite: 183, 184]")

################################################################################
# --- MÓDULO 6: LINKS ÚTEIS ---
################################################################################
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
