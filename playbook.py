import streamlit as st
import pandas as pd
import os
from datetime import datetime
import base64
from pathlib import Path
from google.cloud import firestore
from google.oauth2 import service_account

# --- LÓGICA DE URL (QUERY PARAMS) ---
# 1. Mapeamento de nomes amigáveis para as abas
mapa_urls = {
    "home": "🏠 Home (Equipe)",
    "bonificacao": "💰 Simulador de Bonificação",
    "arquivos": "📄 Biblioteca de Arquivos",
    "scripts": "✍️ Templates & Scripts",
    "politicas": "📊 Políticas Comerciais",
    "problemas": "🛠️ Resolução de Problemas",
    "excuses": "🚫 Quebras de Excuses",
    "resultado": "📈 Impactos no resultado",
    "links": "🔗 Links Úteis",
    "simulador": "🛒 Simulador de Pedidos"
}
# Inverte o mapa para facilitar a busca reversa
mapa_nomes_para_urls = {v: k for k, v in mapa_urls.items()}

# 2. Verifica se existe um parâmetro na URL ao carregar
query_params = st.query_params
aba_da_url = query_params.get("aba", "home")

# 3. Define a aba inicial baseada na URL (se existir)
if 'aba_atual' not in st.session_state:
    st.session_state.aba_atual = mapa_urls.get(aba_da_url, "🏠 Home (Equipe)")

# ------------------------------------------------------------------------------
# CONEXÃO COM O BANCO DE DADOS (FIRESTORE)
# ------------------------------------------------------------------------------
# Esta parte usa os "Secrets" que você salvou no Streamlit Cloud
creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
db = firestore.Client(credentials=creds)

def salvar_no_banco(nova_nota):
    """Salva uma nova ocorrência diretamente na nuvem do Google"""
    # Adiciona à coleção "ocorrencias" no Firestore
    db.collection("ocorrencias").add(nova_nota)

def carregar_do_banco():
    """Puxa todas as ocorrências salvas na nuvem"""
    # Busca os documentos e ordena pelo ID (data/hora de criação)
    try:
        docs = db.collection("ocorrencias").order_by("id_unico", direction=firestore.Query.DESCENDING).stream()
        return [doc.to_dict() for doc in docs]
    except Exception:
        # Retorna lista vazia se ainda não houver dados
        return []

# ------------------------------------------------------------------------------
# EXEMPLO DE USO NO MÓDULO DE OCORRÊNCIAS
# ------------------------------------------------------------------------------
# Quando você for salvar a nota, basta chamar:
# salvar_no_banco(nova_entrada)

# ==========================================
# 🔐 PROTEÇÃO DE ACESSO (F5-PROOF + EXPIRAÇÃO DIÁRIA)
# ==========================================
import streamlit as st
from datetime import date

CODIGO_ACESSO = "maquinadevendas"
token_hoje = f"access_{date.today().strftime('%Y%m%d')}" # Gera algo como 'access_20260331'

# 1. Tenta ler o token de acesso da URL
query_params = st.query_params
acesso_valido = query_params.get("auth") == token_hoje

# 2. Se o token não existir ou for de um dia passado, pede a senha
if not acesso_valido:
    st.title("🔐 Acesso Restrito - Papapá")
    st.info(f"Validação necessária para o dia: {date.today().strftime('%d/%m/%Y')}")
    
    codigo_digitado = st.text_input(
        "Digite o código de acesso",
        type="password"
    )

    if st.button("Entrar"):
        if codigo_digitado == CODIGO_ACESSO:
            # Salva o token com a data de hoje na URL
            st.query_params["auth"] = token_hoje
            st.rerun()
        else:
            st.error("Código incorreto")

    st.stop()

# Botão opcional na barra lateral para limpar o acesso
if st.sidebar.button("Sair (Limpar Sessão)"):
    st.query_params.clear()
    st.rerun()

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

import pandas as pd
from datetime import datetime, timedelta
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday
import streamlit as st
import streamlit.components.v1 as components

################################################################################
# --- 1. CONFIGURAÇÕES DE ESTILO E PÁGINA ---
################################################################################
st.set_page_config(
    page_title="Papapá | Sales Hub 2026", 
    layout="wide", 
    page_icon="💙",
    initial_sidebar_state="collapsed"
)

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

arquivo_logo = "Papapa-azul.png" 
img_base64_oficial = get_base64_of_bin_file(arquivo_logo)
img_logo_html = f"data:image/png;base64,{img_base64_oficial}" if img_base64_oficial else ""

################################################################################
# --- 2. NAVEGAÇÃO HORIZONTAL PADRONIZADA (FLEXBOX) ---
################################################################################

st.markdown(f"""
    <style>
    /* Esconde a sidebar e ajusta o topo */
    [data-testid="stSidebar"] {{ display: none; }}
    .main .block-container {{ padding-top: 2rem; }}

    /* Container do Cabeçalho */
    .header-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin-bottom: 30px;
    }}

    /* --- O SEGREDO DO ALINHAMENTO --- */
    /* Forçamos o container dos botões a usar todo o espaço de forma igual */
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important; /* Distribui espaço igual entre eles */
        align-items: stretch !important;
        gap: 10px !important; /* Distância fixa entre os botões */
    }}

    /* Estilo do Botão */
    .stButton > button {{
        width: 100% !important;
        border-radius: 8px !important;
        height: 4.5em !important; 
        background-color: #f0f2f6 !important;
        color: #1A1C24 !important;
        font-weight: 700 !important;
        font-size: 0.75rem !important; /* Ajuste para não quebrar a linha */
        border: 1px solid #d1d5db !important;
        padding: 5px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    /* Hover e Seleção */
    .stButton > button:hover {{
        border-color: #007bff !important;
        color: #007bff !important;
        background-color: #ffffff !important;
    }}
    </style>

    <div class="header-container">
        <img src="{img_logo_html}" width="300">
        <h1 style='color: #004a99; font-family: sans-serif; font-weight: 850; margin-top: 10px;'>
            Hub - Comercial
        </h1>
    </div>
    """, unsafe_allow_html=True)

# --- 1. MAPEAMENTO DE URLS ---
mapa_urls = {
    "home": "🏠 Home (Equipe)",
    "bonificacao": "💰 Simulador de Bonificação",
    "arquivos": "📄 Biblioteca de Arquivos",
    "scripts": "✍️ Templates & Scripts",
    "politicas": "📊 Políticas Comerciais",
    "problemas": "🛠️ Resolução de Problemas",
    "excuses": "🚫 Quebras de Excuses",
    "resultado": "📈 Impactos no resultado",
    "links": "🔗 Links Úteis",
    "simulador": "🛒 Simulador de Pedidos"
}
mapa_nomes_para_urls = {v: k for k, v in mapa_urls.items()}

# --- 2. SINCRONIZAÇÃO INICIAL (URL -> APP) ---
query_params = st.query_params
aba_da_url = query_params.get("aba", "home")

if 'aba_atual' not in st.session_state:
    # Se a URL tiver algo, carrega essa aba. Se não, vai para Home.
    st.session_state.aba_atual = mapa_urls.get(aba_da_url, "🏠 Home (Equipe)")

# Lista de opções para os botões
opcoes_menu = list(mapa_urls.values())

# --- 3. CRIAÇÃO DOS BOTÕES E ATUALIZAÇÃO DA URL ---
cols = st.columns(len(opcoes_menu))

for i, label in enumerate(opcoes_menu):
    with cols[i]:
        if st.button(label, key=f"btn_{label}", use_container_width=True):
            st.session_state.aba_atual = label
            # Muda o link lá em cima no navegador
            url_slug = mapa_nomes_para_urls.get(label, "home")
            st.query_params["aba"] = url_slug

aba_selecionada = st.session_state.aba_atual
st.divider()
    
################################################################################
# --- MÓDULO 1: HOME (VISUALIZAÇÃO DA EQUIPE REFORMULADA) ---
################################################################################
if aba_selecionada == "🏠 Home (Equipe)":
    st.header("👥 Ecossistema Comercial - Papapá")
    st.write("Conheça o time que faz a operação acontecer.")

    # ESTRUTURA CSS
    st.markdown("""
        <style>
        .team-card {
            background-color: white; 
            padding: 15px; 
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.08); 
            text-align: center;
            margin-bottom: 20px; 
            border: 1px solid #eaeaea;
            height: 360px;
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center;
            transition: transform 0.3s;
        }
        
        .team-card:hover { transform: translateY(-5px); }

        .photo-circle {
            width: 120px; 
            height: 120px; 
            border-radius: 50%;
            border: 4px solid #007bff; 
            margin-bottom: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            background-size: cover;
            background-position: center top;
            background-repeat: no-repeat;
        }

        /* Ajustes de Enquadramento Específicos */
        .photo-joao-vitor { background-position: center 20%; }
        .photo-ana { background-position: center 10%; }
        .photo-priscila { background-position: center 15%; }

        .team-name { font-weight: bold; font-size: 1.05em; color: #333; margin-bottom: 2px; }
        .team-role { color: #666; font-size: 0.85em; margin-bottom: 10px; font-weight: 500; font-style: italic; min-height: 35px; }
        
        .contact-container {
            width: 100%;
            padding-top: 8px;
            border-top: 1px solid #eee;
        }

        .contact-link {
            text-decoration: none !important;
            color: #007bff !important;
            font-size: 0.78em;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }
        
        .whatsapp-icon { width: 14px; height: 14px; }
        .section-title { 
            background: #f0f2f6; 
            padding: 10px; 
            border-radius: 10px; 
            margin: 20px 0; 
            color: #1f3a5f;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

    wa_icon_url = "https://cdn-icons-png.flaticon.com/512/733/733585.png"
    url_avatar_masculino = "https://www.w3schools.com/howto/img_avatar.png"
    url_avatar_feminino = "https://www.w3schools.com/howto/img_avatar2.png"

    # FUNÇÃO INTERNA PARA RENDERIZAR CARDS
    def render_equipe(lista_membros):
        for i in range(0, len(lista_membros), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(lista_membros):
                    m = lista_membros[i + j]
                    num_limpo = "".join(filter(str.isdigit, m['telefone']))
                    link_wa = f"https://web.whatsapp.com/send?phone=55{num_limpo}"
                    
                    # Lógica da Foto com Fallback seguro
                    avatar_padrao = m.get("avatar", url_avatar_masculino)
                    estilo = f"background-image: url('{avatar_padrao}');"
                    
                    if Path(m['foto']).exists():
                        try:
                            f_b64 = get_base64_of_bin_file(m['foto'])
                            estilo = f"background-image: url('data:image/jpeg;base64,{f_b64}');"
                        except:
                            pass
                    
                    with cols[j]:
                        st.markdown(f"""
                            <div class="team-card">
                                <div class="photo-circle {m.get('classe', '')}" style="{estilo}"></div>
                                <div class="team-name">{m['nome']}</div>
                                <div class="team-role">{m['cargo']}</div>
                                <div class="contact-container">
                                    <a href="{link_wa}" target="_blank" class="contact-link">
                                        <img src="{wa_icon_url}" class="whatsapp-icon"> {m['telefone']}
                                    </a>
                                    <a href="mailto:{m['email']}" class="contact-link">
                                        ✉️ {m['email']}
                                    </a>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
    # --- SETOR 0: DIRETOR COMERCIAL ---
    st.markdown('<div class="section-title">👔 Diretor Comercial</div>', unsafe_allow_html=True)
    diretor_comercial = [
        {"nome": "Mariano", "cargo": "Diretor Comercial", "foto": "Mariano.jpeg", "classe": "", "telefone": "(11) 99408-5130", "email": "mariano@papapa.com.br"}
    ]
    render_equipe(diretor_comercial)

    st.markdown("---")


    # --- SETOR 1: INSIDE SALES ---
    st.markdown('<div class="section-title">⚡ Inside Sales</div>', unsafe_allow_html=True)
    inside_sales = [
        {"nome": "João Vitor Tadra", "cargo": "Coordenador", "foto": "João Vitor.jpeg", "classe": "photo-joao-vitor", "telefone": "(41) 98495-9492", "email": "comercial1@papapa.com.br"},
        {"nome": "Ana Christina Rodrigues", "cargo": "Analista - Key Accounts", "foto": "Ana.jpeg", "classe": "photo-ana", "telefone": "(41) 3797-6554", "email": "comercial3@papapa.com.br"},
        {"nome": "Pedro Henrique Born", "cargo": "Analista - Crescimento", "foto": "Pedro.jpeg", "classe": "", "telefone": "(41) 3797-6885", "email": "comercial5@papapa.com.br"},
        {"nome": "Joao Paulo Ferreira Alves", "cargo": "Analista - Desenvolvimento", "foto": "João Paulo.jpeg", "classe": "", "telefone": "(41) 99247-4213", "email": "comercial2@papapa.com.br"},
        {"nome": "Rodrigo Sarlo", "cargo": "Analista - Desenvolvimento", "foto": "rodrigo.jpeg", "classe": "", "telefone": "(41) 98502-7025", "email": "comercial4@papapa.com.br"}
    ]
    render_equipe(inside_sales)

    st.markdown("---")

    st.markdown('<div class="section-title">🤝 CS/Pós-vendas</div>', unsafe_allow_html=True)
    pos_vendas = [
        {"nome": "João Vitor Tadra", "cargo": "Coordenador", "foto": "João Vitor.jpeg", "classe": "photo-joao-vitor", "telefone": "(41) 98495-9492", "email": "comercial1@papapa.com.br"},
        {"nome": "Tassiani Tussolini", "cargo": "Analista - CS", "foto": "Tassiani.jpeg", "classe": "", "telefone": "(41) 98470-3249", "email": "atendimento@papapa.com.br", "avatar": url_avatar_feminino},
        {"nome": "Gesianne Farias", "cargo": "Analista - CS", "foto": "Gesianne.jpeg", "classe": "", "telefone": "(41) 98470-3249", "email": "sac@papapa.com.br", "avatar": url_avatar_feminino},
        {"nome": "Thiago Martins Cabral", "cargo": "Estagiário - Pós-venda", "foto": "Thiago.jpeg", "classe": "", "telefone": "(41) 98502-7025", "email": "comercial4@papapa.com.br"},
        {"nome": "Bernardo Oliveira Dallegrave", "cargo": "Estagiário - Pós-venda", "foto": "Bernardo.jpeg", "classe": "", "telefone": "(41) 98470-3249", "email": "comercial6@papapa.com.br"}
    ]
    render_equipe(pos_vendas)

    

    # --- SETOR 2: ADM VENDAS ---
    st.markdown('<div class="section-title">📊 Administração de Vendas</div>', unsafe_allow_html=True)
    adm_vendas = [
        {"nome": "Priscila de Assis Lima", "cargo": "Analista de Adm Vendas", "foto": "Priscila.jpeg", "classe": "photo-priscila", "telefone": "(41) 98439-0737", "email": "adm.vendas@papapa.com.br"}
    ]
    render_equipe(adm_vendas)

    st.markdown("---")

    # --- SETOR 3: GERENTES REGIONAIS ---
    st.markdown('<div class="section-title">🌍 Gerentes Regionais</div>', unsafe_allow_html=True)
    gerentes = [
        {"nome": "Fernando Andrade", "cargo": "Key Account", "foto": "Fernando.jpeg", "classe": "", "telefone": "(11) 94831-0774", "email": "comercialsp3@papapa.com.br"},
        {"nome": "Tiago Eleuterio", "cargo": "Regional NE", "foto": "Tiago.jpeg", "classe": "", "telefone": "(85) 98759-2781", "email": "comercialne@papapa.com.br"},
        {"nome": "Renato Basso", "cargo": "Regional SP", "foto": "Renato.jpeg", "classe": "", "telefone": "(14) 98807-8888", "email": "comercialsp2@papapa.com.br"},
        {"nome": "Elton Lopes", "cargo": "Regional NCOSE", "foto": "Elton.jpeg", "classe": "", "telefone": "(41) 99212-8370", "email": "comercialmg@papapa.com.br"},
        {"nome": "Felipe Augustus", "cargo": "Regional SUL", "foto": "Felipe.jpeg", "classe": "", "telefone": "(17) 98206-1509", "email": "comercialsul@papapa.com.br"}
    ]
    render_equipe(gerentes)
    
################################################################################
# --- MÓDULO 2: SIMULADOR DE BONIFICAÇÃO ---
################################################################################
elif aba_selecionada == "💰 Simulador de Bonificação":
    st.header("💰 Simulador de Bonificação Individual - Inside Sales")
    
    col_input, col_result = st.columns([1, 1.5])
    
    with col_input:
        # Trocamos value por None e adicionamos o placeholder
        salario_base = st.number_input(
            "Seu Salário Fixo Base (R$)", 
            min_value=0.0, 
            value=None, 
            placeholder="Preencha aqui seu salário"
        )
        meta_mes = st.number_input(
            "Valor da Meta do Mês (R$)", 
            min_value=0.0, 
            value=None, 
            placeholder="Preencha aqui sua meta do mês"
        )
        resultado_atual = st.number_input(
            "Seu Resultado Atual Batido (R$)", 
            min_value=0.0, 
            value=None, 
            placeholder="Preencha aqui seu resultado atual"
        )
        
    with col_result:
        # Só realiza o cálculo se os campos não estiverem vazios
        if salario_base is not None and meta_mes is not None and resultado_atual is not None:
            atingimento = (resultado_atual / meta_mes) * 100 if meta_mes > 0 else 0.0
            
            if atingimento >= 110.0:
                perc_bonus, status_meta, cor_metric = 0.30, " Superação (110%+)!", "normal"
            elif atingimento >= 90.0:
                perc_bonus, status_meta, cor_metric = 0.20, " No Piso (90-109%)", "normal"
            else:
                perc_bonus, status_meta, cor_metric = 0.0, " Abaixo do Piso (<90%)", "inverse"
                
            valor_bonus = salario_base * perc_bonus
            total_estimado = salario_base + valor_bonus
            
            st.metric(label="Atingimento da Meta", value=f"{atingimento:.1f}%", delta=status_meta, delta_color=cor_metric)
            
            c1, c2 = st.columns(2)
            with c1:
                st.metric(label="Valor do Bônus", value=f"R$ {valor_bonus:,.2f}", delta=f"{perc_bonus*100:.0f}% sobre o fixo")
            with c2:
                st.metric(label="Total Estimado", value=f"R$ {total_estimado:,.2f}")
        else:
            # Mensagem amigável enquanto o usuário não preenche
            st.info("Insira os valores ao lado para calcular sua bonificação automaticamente.")

################################################################################
# --- MÓDULO 3: BIBLIOTECA DE ARQUIVOS ---
################################################################################
elif aba_selecionada == "📄 Biblioteca de Arquivos":
    st.header("📄 Biblioteca de Arquivos")
    
    # Criando 4 colunas para colocar tudo na mesma linha
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.subheader("📁 Materiais de Venda")
        arquivos_venda = {
            "📖 Catálogo Digital (PDF)": "catalogo-papapa-digital.pdf",
            "💰 Tabela de Preços - Padrão (Excel)": "0626E - Tabela de Preços - Papapá 2.0.xlsx",
            "🕸️ Tabela de Preços - Rede (Excel)": "0626ER - Tabela de Preços Rede - Papapá 2.0.xlsx",
            "ℹ️ Ficha Técnica de Produtos": "Informações todos os produtos Papapá.pdf",
            "🍎 Guia de Produtos": "https://drive.google.com/file/d/1ulatv5WYZZJYubylJ_SfWoPsdbOVFgHR/view?usp=sharing",
            "📄 Fichas comerciais dos produtos": "https://papapacombr.sharepoint.com/sites/Papapa-Fileserver/Documentos%20Compartilhados/Forms/AllItems.aspx?id=%2Fsites%2FPapapa%2DFileserver%2FDocumentos%20Compartilhados%2FComercial%2F0%20%2D%20COMERCIAL%2F10%20%2D%20Ficha%20cadastral%20de%20produtos%2FFicha%20comercial%20de%20produto&viewid=49270ad9%2D7603%2D4cc9%2Dbc50%2Dbb5ddf155cf9&p=true&ct=1776971104130&or=Teams%2DHL&LOF=1"
        }
        for label, path in arquivos_venda.items():
            if path.startswith("http"):
                # Se for link, usa link_button
                st.link_button(label, path, use_container_width=True, key=f"link_{label}")
            else:
                # Se for arquivo, tenta o download_button
                try:
                    with open(path, "rb") as f:
                        st.download_button(label, f, file_name=path, use_container_width=True, key=f"venda_{path}")
                except FileNotFoundError: 
                    st.error(f"Pendente: {label}")

    with col2:
        st.subheader("📋 Guias e Processos")
        arquivos_proc = {
            "🎯 Estrutura de Operação e Metas": "Estrutura de Operação e Metas - Inside Sales.pdf",
            "📦 Guia de Recebimento de Mercadorias": "GUIA DE RECEBIMENTO DE MERCADORIAS.pdf",
            "🔄 Orientações para emissão de NFD": "Orientações para emissão da Nota Fiscal de Devolução (1) (3).pdf",
            "📝 Templates (PDF)": "Templates IS 2026.docx (2).pdf",
            "📊 Central de Templates - Reativação": "Central de Templates Comercial - PAPAPÁ.xlsx",
            "📄 Central de Templates - Recuperação": "[Atualizada ] Central de Templates Comercial Expansão de Carteira- PAPAPÁ.xlsx",
            "🧩 Sales Planning Framework": "[PAPAPÁ] - Sales Planning Framework.xlsx"
        }
        for label, path in arquivos_proc.items():
            try:
                with open(path, "rb") as f:
                    st.download_button(label, f, file_name=path, use_container_width=True, key=f"proc_{path}")
            except FileNotFoundError: st.error(f"Pendente: {label}")

    with col3:
        st.subheader("🏦 Docs Fiscais")
        arquivos_fiscais = {
            "📄 Ata AGE 2025": "2025_07_08, Baby Roo, Ata AGE 2025, mudança sede e matriz, versão JUCEPAR, WSA, Registrada.pdf",
            "✅ CND - Federais": "- CND – Certidão Negativa de Débitos Federais 1.pdf",
            "🏙️ CND - Municipais": "CND MUNICIPAL - BABY ROO.pdf",
            "👨‍🚒 Alvará Bombeiro - Venc 04/11/2026": "BABY ROO - CVCB Bombeiro - venc 04.11.2026.pdf",
            "💳 Cartão CNPJ": "CARTÃO CNPJ BABY ROO.pdf",
            "🏛️ Inscrição Municipal": "INSCRIÇÃO MUNICIPAL.pdf",
            "📑 Sintegra": "SINTEGRA PAPAPÁ.pdf",
            "💰 Comprovante Bancário": "COMPROVANTE BANCÁRIO (1).png",
            "🏥 Licença sanitária - Venc 10/11/2027": "Licença Sanitária_Baby Roo - Val 10.11.27.pdf"
        }
        for label, path in arquivos_fiscais.items():
            try:
                with open(path, "rb") as f:
                    st.download_button(label, f, file_name=path, use_container_width=True, key=f"fisc_{path}")
            except FileNotFoundError: st.error(f"Pendente: {label}")

    with col4:
        st.subheader("🎓 Treinamentos")
        arquivos_treinamento = {
            "📊 Atendimento ao Cliente": "Atendimento ao cliente.pptx",
            "🎯 CS & Vendas": "CS & Vendas.pptx",
        }
        for label, path in arquivos_treinamento.items():
            try:
                with open(path, "rb") as f:
                    st.download_button(label, f, file_name=path, use_container_width=True, key=f"treino_{path}")
            except FileNotFoundError: st.error(f"Pendente: {label}")

    st.divider()

    # BLOCO: TELEFONES VEKTA
    st.markdown("""
        <div class="vekta-panel">
            <div class="vekta-title">📞 Telefones cadastrados na Vekta</div>
            <table class="vekta-table">
                <tr><td><b>João Tadra</b></td><td>5541998106275</td></tr>
                <tr><td><b>Pedro</b></td><td>554137976885</td></tr>
                <tr><td><b>Ana</b></td><td>5541999029246</td></tr>
                <tr><td><b>João Paulo</b></td><td>5541992474213</td></tr>
                <tr><td><b>Thiago</b></td><td>5541985027025</td></tr>
                <tr><td><b>Bernardo</b></td><td>5541996503745</td></tr>
            </table>
        </div>
    """, unsafe_allow_html=True)

################################################################################
# --- MÓDULO 4: TEMPLATES & SCRIPTS ---
################################################################################
elif aba_selecionada == "✍️ Templates & Scripts":
    st.header("✍️ Templates & Scripts")
    st.markdown("💡 **Dica:** Use os botões no canto superior direito de cada bloco para copiar o texto rapidamente.")
    
    tabs = st.tabs([
        "🤝 Abordagem Inicial", 
        "🚀 Explicação de Mix (Curva A)", 
        "📝 Cadastro & Fechamento", 
        "🚚 Pós-Venda & Financeiro",
        "🔄 Recuperação",
        "📈 Expansão"
    ])
    
    # --- ABA 0: ABORDAGEM ---
    with tabs[0]:
        st.subheader("📞 Primeiro contato (leads)")
        
        with st.expander("⭐ Opção 1: Abordagem consultiva", expanded=True):
            st.code("""Olá, tudo bem?
Aqui é [SEU NOME], da Papapá.
Vi que você se cadastrou na nossa página e quis entrar em contato para entender um pouco melhor o seu perfil e te indicar as melhores opções do nosso portfólio.
Você poderia me contar rapidamente que tipo de estabelecimento você tem?""", language=None)

        with st.expander("🏢 Opção 2: Foco em perfil de negócio"):
            st.code("""Oi, tudo bem?
Sou [SEU NOME], da Papapá.
Que legal ver seu interesse em trabalhar com nossos produtos!
Antes de te apresentar o portfólio completo, queria entender um pouco mais sobre o seu negócio, para te indicar as melhores opções e condições.
Você pode me contar rapidamente como funciona hoje?""", language=None)

        with st.expander("✅ Opção 3: Perguntas de qualificação (checklist)"):
            st.code("""Antes de te indicar os produtos, queria entender rapidinho:
• Que tipo de estabelecimento você tem?
• Em qual cidade/bairro?
• Seu público é mais família, fitness ou geral?""", language=None)

        with st.expander("📩 Opção 4: Abordagem mais direta"):
            st.code("""Olá, tudo bem? Aqui é [SEU NOME], da Papapá.
Recebi seu cadastro e quis agradecer pelo interesse. A Papapá trabalha com uma linha de alimentação natural e pronta para bebês e crianças, sem conservantes e com ótima aceitação.
Posso te enviar o catálogo e as condições comerciais e, na sequência, entender se faz sentido para o seu negócio?""", language=None)

    # --- ABA 1: CURVA A ---
    with tabs[1]:
        st.subheader("🚀 Como explicar o Mix e Giro")
        st.info("Use estes scripts para converter clientes que estão em dúvida sobre o que comprar no primeiro pedido.")
        
        with st.expander("💎 Script 1: A força da curva A (resumido)", expanded=True):
            st.code("""Pra te orientar melhor, vou te explicar como funciona o nosso mix e por onde indicamos começar. 
Hoje, a nossa Curva A (maior giro e recompra) é formada por:

• Papinhas de fruta – Nosso carro-chefe. Naturais, sem açúcar e não precisam de refrigeração.
• Biscoito Dentição – Snack funcional muito procurado por pais, com ótima saída por impulso.
• Biscotti – Nosso snack mais vendido, agrada bebês e até adultos.

Normalmente, quando o cliente começa pela Curva A, ele sente o giro rápido e depois amplia o mix com Palitinhos e Yoguzinho para aumentar o ticket médio.""", language=None)

        with st.expander("📚 Script 2: Explicação curva A (mais completa)"):
            st.code("""Pra te orientar melhor, vou te explicar rapidamente como funciona o nosso mix e por onde normalmente indicamos começar.

Hoje, a nossa Curva A (produtos de maior giro e recompra) é formada por:
• Papinhas de fruta – carro-chefe da marca, porta de entrada da maioria dos clientes. São naturais, sem adição de açúcar, não precisam de refrigeração e têm excelente aceitação.
• Biscoitinho para fase da dentição – snack funcional, muito procurado por pais de bebês, com compra recorrente e ótima saída por impulso.
• Biscotti – nosso snack mais vendido, feito com cereais selecionados, naturalmente adocicado pelas frutas e com perfil que agrada até adultos.

Esses três itens concentram hoje a maior parte do volume da Papapá no ponto de venda e são os que mais performam em praticamente todos os canais (padarias, empórios, hortifruttis e mercados).

Em um segundo momento, como complemento de mix e aumento de ticket, entram:
• Palitinhos de vegetais – assados, não fritos, fonte de proteínas e ideais para lanchinho.
• Yoguzinho – produto super diferenciado, que não precisa de refrigeração antes de abrir, com shelf life de 15 meses, perfeito para exposição em gôndola.

Normalmente, quando o cliente começa pela Curva A, ele já consegue sentir giro rápido e recompra, e depois amplia o mix com esses complementares. A partir do seu perfil de negócio, eu te ajudo a montar um pedido inicial enxuto, estratégico e com foco em giro.""", language=None)

        with st.expander("🛒 Script 3: Pergunta para entender o primeiro pedido"):
            st.code("""Pelo seu perfil, o que faz mais sentido é começar com a Curva A. São os produtos de "tiro certo". 
Hoje você imagina algo mais como um teste inicial ou já pensa em abastecer a gôndola para ter uma exposição completa?""", language=None)

    # --- ABA 2: CADASTRO ---
    with tabs[2]:
        st.subheader("📝 Fechamento de Venda")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 📋 Dados para Cadastro")
            st.code("""Para darmos sequência, preciso de:
• CNPJ:
• Inscrição Estadual (IE):
• Telefone Financeiro e Compras:
• E-mail Financeiro e Compras:
• Dados Bancários (pix):

*Obs.: O CNAE deve permitir a comercialização de produtos alimentícios.""", language=None)
            
        with c2: 
            st.markdown("### 💰 Condições Comerciais")
            st.code("""Vou te passar nossas condições para você se organizar:

• Pedido mínimo: R$ 800,00.
• Frete: CIF (Grátis) para todo o Brasil.
• Pagamento: Pix ou Boleto.

Venda por caixas fechadas:
- Yoguzinho e Palitinhos: 16 unidades
- La Chef e Sopinhas: 6 unidades
- Papinhas (Fruta/Carne): 12 unidades
- Dentição, Macarrão, Cereal e Biscotti: 12 unidades""", language=None)
        
        st.divider()
        st.markdown("### 🏦 Dados Bancários Oficiais (Para envio)")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.success("**Chave PIX (CNPJ)**")
            st.code("34.282.307/0001-44")
        with col_b2:
            st.info("**Dados Itaú**")
            st.code("Ag: 8931 | CC: 05510-0\nBABY ROO COMERCIO DE ALIMENTOS S/A")

    # --- ABA 3: PÓS-VENDA ---
    with tabs[3]:
        st.subheader("🚚 Suporte, Logística e Financeiro")
        
        with st.expander("📦 Script: Confirmação e fluxo logístico", expanded=True):
            st.code("""Pedido efetuado com sucesso! Nosso fluxo funciona assim:
• Até 3 dias úteis para separação no CD.
• Mais 2 dias úteis para faturamento da NF.
• Em seguida, coleta da transportadora.
As NFs e boletos chegam direto no seu e-mail cadastrado!""", language=None)

        with st.expander("🚨 Script: Instruções de recebimento"):
            st.warning("Envie este texto SEMPRE que o pedido for faturado.")
            st.code("""Uma orientação importante sobre o recebimento:
No momento da entrega, confira a mercadoria ANTES de assinar o canhoto.
Se houver caixa amassada, molhada ou produto quebrado:
1. Registre a RESSALVA no canhoto da Nota Fiscal que fica com a transportadora descrevendo o erro.
2. Não aceite os produtos avariados.
3. Me informe imediatamente.
Sem a ressalva na NF, a transportadora não aceita a reclamação e não conseguimos realizar o abatimentos nos boletos.""", language=None)

        with st.expander("💳 Script: Contato financeiro"):
            st.code("""Para assuntos financeiros, como boletos, notas fiscais, comprovantes de pagamento, prorrogação de vencimento ou segunda via, pedimos por gentileza que o contato seja feito diretamente com o nosso financeiro, através do e-mail:
📧 E-mail: contasareceber2@papapa.com.br""", language=None)

        with st.expander("🔄 Script: Regra de troca (validade)"):
            st.code("""Sobre trocas por validade:
A Papapá realiza a troca de produtos caso sejam entregues com menos de 60% da sua validade total.
Para iniciarmos a análise, precisamos que nos envie o lote, a validade e a data de recebimento das mercadorias.

Se a análise confirmar que o produto foi entregue com menos de 60% da sua validade total, entraremos em contato para que vocês emitam a Nota Fiscal de Devolução (NFD), que deve conter:
- Número da NF de origem;
- Motivo da devolução;
- Lote do produto.""", language=None)

    # --- ABA RECUPERAÇÃO ---
    with tabs[4]:
        st.subheader("🔄 Estratégias de Recuperação de Clientes")
        st.caption("Utilize estes scripts para reativar parceiros que já conhecem a Papapá.")

        # Exemplo 1: Focado aumentar o mix Completo
        with st.expander("📱 Whatsapp: foco em ticket médio", expanded=True):
            st.code("""Bom dia {{Nome_lead}}!
Passando para compartilhar um ponto estratégico com você: notamos que lojas que trabalham o mix completo (papinhas + cereais + snacks) conseguem elevar o ticket médio, pois o cliente encontra a solução total de introdução alimentar em um só lugar.
Pequenos ajustes no mix evitam que o cliente procure a rede vizinha por falta de opção. Podemos conversar sobre essa estratégia de aumento do ticket médio?""", language=None)

        # Exemplo 2: Focado em giro e ruptura
        with st.expander("📞 Ligação: reativação por giro de categoria"):
            st.code("""Olá, tudo bem? Aqui é o {{seu_nome}}, da Papapá.
Notei que a sua frequência de pedidos tem oscilado. No canal {{segmento do cliente}}, a ruptura na categoria infantil é crítica, pois os pais buscam confiança e conveniência. 
Queria te mostrar como nossa estratégia de reposição evita que você perca venda por falta de produto e garanta a fidelidade do cliente. Podemos falar agora sobre isso?""", language=None)

        # Exemplo 3: Roteiro de Nova Oportunidade (Atualizado)
        with st.expander("🎯 Script: nova oportunidade de receita"):
            st.code("""Olá {{Nome_lead}}, tudo bem?
Eu sou {{seu_nome}}, faço parte do time da Papapá.
Estou retornado nosso contato pois quero lhe apresentar uma forma de deixar os produtos da Papapá dentro da sua operação e criar uma nova oportunidade de receita para você.
Posso te ligar para uma conversa rápida de 10 minutos?""", language=None)

        st.markdown("---")
        st.subheader("📊 Material de Apoio - Recuperação")
        
        # O botão de download agora está corretamente identado dentro da tabs[4]
        nome_arquivo = "Central de Templates Comercial - PAPAPÁ.xlsx"
        try:
            with open(nome_arquivo, "rb") as file:
                st.download_button(
                    label="📥 Baixar Templates de Recuperação",
                    data=file,
                    file_name=nome_arquivo,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    help="Clique para baixar a planilha com todos os scripts de abordagem e recuperação."
                )
        except FileNotFoundError:
            st.error("Arquivo de templates não encontrado no diretório do servidor.")

          # --- ABA EXPANSÃO ---
    with tabs[5]:
        st.subheader("📈 Estratégias de Expansão de Carteira")
        st.caption("Utilize estes scripts para aumentar frequência, giro e presença dentro dos clientes ativos.")

        # Script 1
        with st.expander("📦 Reposição com urgência (giro de final de semana)", expanded=True):
            st.code("""Olá {Nome_lead}, tudo bem?
Eu sou {seu_nome}, faço parte do time da Papapá.
Estou acompanhando o calendário de reposição da {Empresa do lead} e vi que já faz {XX} dias desde o último lote, e não quero que falte produto para o fluxo do final de semana.
Como está a saída nas prateleiras?""", language=None)

        # Script 2
        with st.expander("📊 Planejamento + novos lançamentos"):
            st.code("""Assunto: Planejamento de Categoria e Futuros Lançamentos.

Olá {Nome do lead}, tudo bem?
Estou entrando em contato para confirmar se chegou tudo certinho no seu último pedido!
Vou aproveitar para lhe enviar uma sugestão de reposição focada em manter o seu fluxo de caixa saudável, pois teremos lançamentos logo em breve!
O que acha de darmos uma olhada nessa reposição para garantir que você não fique sem giro e perca vendas para a concorrência?""", language=None)

        # Script 3
        with st.expander("⚡ Fechamento rápido de reposição"):
            st.code("""{Nome_lead}, tudo bem?
Sobre seu último pedido aqui na Papapá, não deixe para a última hora sua reposição.
Quero agilizar seu faturamento para você focar na gestão da loja, e enquanto isso eu cuido para que o seu mix infantil seja o mais completo da região.
Vamos garantir esse pedido ainda hoje?""", language=None)

        st.markdown("---")
        st.subheader("📊 Material de Apoio - Expansão")

        nome_arquivo_expansao = "[Atualizada ] Central de Templates Comercial Expansão de Carteira- PAPAPÁ.xlsx"
        try:
            with open(nome_arquivo_expansao, "rb") as file:
                st.download_button(
                    label="📥 Baixar Templates de Expansão",
                    data=file,
                    file_name=nome_arquivo_expansao,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    help="Clique para baixar a planilha com os scripts de expansão de carteira."
                )
        except FileNotFoundError:
            st.error("Arquivo de expansão não encontrado no diretório do servidor.")      

################################################################################
# --- MÓDULO 5: POLÍTICAS COMERCIAIS ---
################################################################################
elif aba_selecionada == "📊 Políticas Comerciais":
    st.header("📊 Políticas Comerciais - Inside Sales")
    
    # Destaques Rápidos
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pedido Mínimo", "R$ 800,00")
    c2.metric("Frete", "CIF (Grátis)")
    c3.metric("Prazo Saída", "5 dias úteis")
    c4.metric("Troca", "> 60% Shelf Life")

    st.divider()

    col_info1, col_info2 = st.columns(2)

    with col_info1:
        # Estilos CSS
        st.markdown("""
            <style>
            .unidade-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 8px 15px;
                margin-bottom: 5px;
                background-color: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #FF4B4B;
            }
            .unidade-nome { font-weight: 500; color: #31333F; }
            .unidade-valor {
                font-weight: bold; color: #FF4B4B; background: #ffebeb;
                padding: 2px 8px; border-radius: 5px;
            }
            </style>
        """, unsafe_allow_html=True)

        # 1. VALIDADES
        st.subheader("📅 Shelf Life (Validades)")

        st.write("**💙 Papapá**")
        st.markdown("""
            <div class="unidade-row"><span class="unidade-nome">🥩 Papinhas de Carne</span><span class="unidade-valor">12 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">🍼 Yoguzinho</span><span class="unidade-valor">15 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">🍎 Papinhas de Fruta</span><span class="unidade-valor">16 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">🥖 Palitinhos</span><span class="unidade-valor">9 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">🦷 Dentição</span><span class="unidade-valor">15 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">🍝 Macarrão</span><span class="unidade-valor">14 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">👨‍🍳 La Chef</span><span class="unidade-valor">16 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">🌾 Cereal</span><span class="unidade-valor">12 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">🍪 Biscotti</span><span class="unidade-valor">10 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">🥣 Sopinhas</span><span class="unidade-valor">12 meses</span></div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="margin-top: 25px;"></div>', unsafe_allow_html=True)
        st.write("**✨ Era Uma Vez**")
        st.markdown("""
            <div class="unidade-row"><span class="unidade-nome">🥨 Salgadinhos</span><span class="unidade-valor">9 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">🍩 Biscoito Recheado</span><span class="unidade-valor">10 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">🧃 Sucos</span><span class="unidade-valor">8 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">☕ Achocolatado</span><span class="unidade-valor">6 meses</span></div>
        """, unsafe_allow_html=True)

        st.caption("❄️ Nenhuma linha necessita de refrigeração.")
        st.write("") 

        # 2. UNIDADES POR CAIXA
        st.subheader("📦 Unidades por Caixa")

        st.write("**💙 Papapá**")
        st.markdown("""
            <div class="unidade-row"><span class="unidade-nome">🥩 Papinhas de Carne</span><span class="unidade-valor">12 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">🍼 Yoguzinho</span><span class="unidade-valor">16 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">🍎 Papinhas de Fruta</span><span class="unidade-valor">12 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">🥖 Palitinhos</span><span class="unidade-valor">16 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">🦷 Dentição</span><span class="unidade-valor">12 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">🍝 Macarrão</span><span class="unidade-valor">12 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">👨‍🍳 La Chef</span><span class="unidade-valor">6 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">🌾 Cereal</span><span class="unidade-valor">12 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">🍪 Biscotti</span><span class="unidade-valor">12 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">🥣 Sopinhas</span><span class="unidade-valor">6 un.</span></div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="margin-top: 25px;"></div>', unsafe_allow_html=True)
        st.write("**✨ Era Uma Vez**")
        st.markdown("""
            <div class="unidade-row"><span class="unidade-nome">🥨 Salgadinhos</span><span class="unidade-valor">18 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">🍩 Biscoito Recheado</span><span class="unidade-valor">8 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">🧃 Sucos</span><span class="unidade-valor">27 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">☕ Achocolatado</span><span class="unidade-valor">27 un.</span></div>
        """, unsafe_allow_html=True)

    with col_info2:
        st.subheader("💳 Modalidades de Pagamento - Inside Sales")

        st.warning("""
        ⚠️ **Pagamento apenas via PIX no ato do pedido para:**
        * **CNPJs com protestos:** consulte no [CENPROT](https://www.pesquisaprotesto.com.br/).
        * **CNPJs com menos de 1 ano de abertura:** consulte no [SINTEGRA](http://www.sintegra.gov.br/).
        """)
        
        st.markdown("""
            <style>
            .pagamento-texto { font-size: 16px; line-height: 1.6; color: #31333F; }
            .highlight { background-color: #f0f2f6; padding: 2px 6px; border-radius: 4px; font-weight: bold; }
            </style>
        """, unsafe_allow_html=True)

        with st.expander("Prazos: Sul, SP e RJ", expanded=True):
            st.markdown("""
            <div class="pagamento-texto">
            • <b>Até R$ 1.000:</b> <span class="highlight">30 dias da data do faturamento</span><br>
            • <b>R$ 1.000 a R$ 2.000:</b> <span class="highlight">30/45 dias da data do faturamento</span><br>
            • <b>Acima de R$ 2.000:</b> <span class="highlight">30/45/60 dias da data do faturamento</span>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Prazos: Demais Regiões", expanded=True):
            st.markdown("""
            <div class="pagamento-texto">
            • <b>Até R$ 1.000:</b> <span class="highlight">45 dias da data do faturamento</span><br>
            • <b>R$ 1.000 a R$ 2.000:</b> <span class="highlight">45/60 dias da data do faturamento</span><br>
            • <b>Acima de R$ 2.000:</b> <span class="highlight">40/50/60 dias da data do faturamento</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.success("**Pagamento:** PIX ou Boleto")

        st.markdown("### 🏦 Dados Bancários Oficiais (Para envio)")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.success("**Chave PIX (CNPJ)**")
            st.code("34.282.307/0001-44")
        with col_b2:
            st.info("**Dados Itaú**")
            st.code("Ag: 8931 | CC: 05510-0\nBABY ROO COMERCIO DE ALIMENTOS S/A")

        st.markdown("---")

        # --- MODALIDADES REGIONAIS ---
        st.subheader("💼 Modalidades de Pagamento - Regionais")
        
        st.info("💡 **Política Comercial:** Os prazos e condições para vendas via Gerentes Regionais são definidos **conforme negociação direta com o cliente** ou especificações contidas no pedido enviado.")

        with st.expander("📝 Prazos e Condições Genéricas", expanded=True):
            st.markdown("""
            <div class="pagamento-texto">
            • <b>Faturamento Direto:</b> Conforme acordado em contrato ou pedido.<br>
            • <b>Análise de Crédito:</b> Sujeito à aprovação pelo financeiro conforme histórico do cliente.<br>
            • <b>Flexibilidade:</b> Condições especiais para Redes e Key Accounts sob consulta.
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("""
            <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #1f3a5f;">
                <p style="margin: 0; font-size: 14px; color: #1f3a5f;">
                <b>Nota:</b> Toda e qualquer divergência nas modalidades de pagamento deve ser validada junto ao setor de <b>Administração de Vendas</b> antes da finalização do pedido.
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="margin-top: 25px;"></div>', unsafe_allow_html=True)

        st.markdown("---")

        st.subheader("🔄 Trocas e Devoluções")
        st.warning("""
        **Validade:** Troca aplicada apenas se o produto chegar com **menos de 60%** do Shelf Life total.
        
        **Avarias/Faltas:** No ato da entrega, é **obrigatório realizar a ressalva no verso da Nota Fiscal** apontando o motivo.
        
        **Documentação:** Necessário envio da NFD (Nota Fiscal de Devolução) citando a NF de origem e motivo da devolução.
        """)
        
        st.info("💡 **Dica:** Oriente o lojista a conferir a mercadoria com o transportador presente.")

        # --- CONSULTA DINÂMICA DE PRAZO (VIA PLANILHA) ---
        st.write("") 
        st.markdown("#### ⏱️ Consulta de Prazo por Cidade")

        try:
            import pandas as pd
            
            # 1. Carrega especificando a aba correta: "tabela de lead time"
            df_prazos = pd.read_excel("Tabela lead time operacao e comercial.xlsx", sheet_name="tabela de lead time")
            
            # 2. Remove linhas que estejam totalmente vazias (previne erro de conversão)
            df_prazos = df_prazos.dropna(subset=['Cidade', 'UF', 'Lead time total'])
            
            # 3. Criamos a coluna formatada
            df_prazos['Exibicao'] = df_prazos['Cidade'].astype(str).str.strip() + " (" + df_prazos['UF'].astype(str).str.strip() + ")"
            opcoes_cidades = sorted(df_prazos['Exibicao'].unique())
            
            cid_sel = st.selectbox(
                "Selecione a Cidade:", 
                opcoes_cidades, 
                index=None, 
                placeholder="Busque aqui a cidade...",
                label_visibility="collapsed"
            )
            
            if cid_sel:
                # Busca o valor
                valor_raw = df_prazos[df_prazos['Exibicao'] == cid_sel]['Lead time total'].values[0]
                
                # Converte para inteiro (garante que remova o .0)
                dias_est = int(float(valor_raw))
                
                st.markdown(f"""
                    <div style="background-color: #e8f4f8; padding: 15px; border-radius: 10px; border-left: 5px solid #29b5e8; text-align: center;">
                        <span style="color: #1f77b4; font-size: 14px; font-weight: bold;">PREVISÃO TOTAL</span><br>
                        <span style="font-size: 24px; font-weight: bold; color: #31333F;">{dias_est} dias úteis</span>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.caption("Aguardando seleção de cidade...")

        except Exception as e:
            st.error(f"Erro ao carregar a tabela de prazos.")
            # st.write(e) # Descomente esta linha se o erro persistir para ver o motivo técnico

    st.divider()

# --- SEÇÃO: GLOSSÁRIO ---
    st.subheader("📖 Glossário de Vendas & Distribuição")
    st.write("Consulte os termos e siglas essenciais da operação Inside Sales da Papapá.")

    # CSS para os mini-cards do glossário
    st.markdown("""
        <style>
        .glossary-card {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #eee;
            margin-bottom: 15px;
            height: 100%;
        }
        .glossary-category {
            color: #007bff;
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .glossary-item {
            margin-bottom: 8px;
            font-size: 0.92em;
        }
        .glossary-term {
            font-weight: bold;
            color: #333;
        }
        </style>
    """, unsafe_allow_html=True)

    # Função auxiliar para renderizar os itens
    def item_glossario(termo, definicao):
        return f'<div class="glossary-item"><span class="glossary-term">{termo}:</span> {definicao}</div>'

    # Divisão em colunas para melhor aproveitamento da tela
    col1, col2 = st.columns(2)

    with col1:
        # Mercado e Distribuição
        st.markdown(f"""
            <div class="glossary-card">
                <div class="glossary-category">🛒 Mercado & Distribuição</div>
                {item_glossario("PDV (Ponto de Venda)", "Loja ou varejista que revende produtos ao consumidor final.")}
                {item_glossario("Shopper", "Cliente final que compra para uso pessoal (pessoa física).")}
                {item_glossario("Markup", "Percentual adicionado ao custo para formar o preço de venda.")}
                {item_glossario("Preço Sugerido", "Valor recomendado pelo fabricante para venda ao PDV ou consumidor.")}
                {item_glossario("Sell-in", "Vendas da Papapá para o distribuidor ou PDV.")}
                {item_glossario("Sell-out", "Vendas reais do PDV para o shopper final.")}
                {item_glossario("Consumidor", "Aquele que efetivamente utiliza o produto, podendo ser diferente do Shopper que realizou a compra.")}
                {item_glossario("Ruptura", "Falta de produto na gôndola ou no estoque do PDV, impedindo a venda ao shopper.")}
                {item_glossario("Share de Gôndola", "Espaço que a marca ocupa na prateleira do PDV em relação aos concorrentes.")}
            </div>
        """, unsafe_allow_html=True)

        # Prospecção e Qualificação
        st.markdown(f"""
            <div class="glossary-card" style="margin-top: 15px;">
                <div class="glossary-category">🔍 Prospecção & Qualificação</div>
                {item_glossario("Inbound Marketing", "Estratégia de atração passiva baseada na criação de conteúdo para que o cliente chegue até a empresa.")}
                {item_glossario("Outbound Sales", "Estratégia de prospecção ativa onde a empresa vai até o cliente através de abordagens diretas.")}
                {item_glossario("BANT", "Critério de qualificação (Budget, Authority, Need, Timeline).")}
                {item_glossario("Rapport", "Técnica de criar ligação, empatia e confiança mútua com o interlocutor.")}
                {item_glossario("Cold Call/Mail", "Contato inicial não solicitado para gerar interesse.")}
                {item_glossario("Lead", "Pessoa ou empresa que demonstrou interesse ou tem perfil para se tornar um cliente.")}
                {item_glossario("ICP (Ideal Customer Profile)", "Perfil de Cliente Ideal; descrição da empresa ou pessoa que mais se beneficia da sua solução.")}
                
                
            </div>
        """, unsafe_allow_html=True)

        # Processo de Vendas
        st.markdown(f"""
            <div class="glossary-card" style="margin-top: 15px;">
                <div class="glossary-category">⚙️ Processo de Vendas</div>
                {item_glossario("B2C (Business to Consumer)", "Modelo de negócio focado na venda direta para o consumidor final.")}
                {item_glossario("B2B (Business to Business)", "Modelo de negócio onde empresas vendem produtos ou serviços para outras empresas.")}
                {item_glossario("CRM (Customer Relationship Management)", "Software utilizado para gerenciar todo o relacionamento e histórico com os clientes.")}
                {item_glossario("Ticket Médio", "Valor médio das vendas realizadas, calculado dividindo o faturamento pelo número de pedidos.")}
                {item_glossario("Conversion Rate (Taxa de Conversão)", "Percentual de leads ou oportunidades que avançam de uma etapa para a próxima no funil.")}
                {item_glossario("Win Rate (Taxa de Vitórias)", "Métrica que calcula o percentual de negócios fechados em relação ao total de oportunidades criadas.")}
                {item_glossario("Lost Rate (Taxa de Perda)", "Percentual de oportunidades que foram descartadas ou perdidas durante o processo de venda.")}
                {item_glossario("Forecast", "Previsão de vendas para um período futuro baseada nas oportunidades do pipeline.")}
                {item_glossario("Follow-up", "Ação de manter contato com um lead após uma abordagem inicial para incentivar a conversão.")}
                {item_glossario("Pipeline", "Visão das etapas do funil (prospecção até fechamento).")}
                {item_glossario("MQL / SQL / SAL", "Estágios de qualificação do lead (Marketing, Vendas e Aceito).")}
                {item_glossario("Ramp-up", "Período para um vendedor atingir produtividade plena.")}
            </div>
        """, unsafe_allow_html=True)

    with col2:
        # Logística e Identificação
        st.markdown(f"""
            <div class="glossary-card">
                <div class="glossary-category">📦 Logística & Identificação</div>
                {item_glossario("Lead Time", "Tempo total entre o pedido do cliente e a entrega efetiva do produto.")}
                {item_glossario("SKU (Stock Keeping Unit)", "Código interno alfanumérico único para gerenciar estoque.")}
                {item_glossario("Last Mile (Última Milha)", "Etapa final do transporte, quando o produto sai do centro de distribuição para o destino final.")}
                {item_glossario("Picking", "Processo de separação e coleta dos produtos no estoque para preparar um pedido.")}
                {item_glossario("Packing", "Processo de embalagem e acomodação dos produtos para que sejam transportados com segurança.")}
                {item_glossario("FIFO / PEPS", "Método de gestão de estoque onde o primeiro produto a entrar é o primeiro a sair (essencial para perecíveis).")}
                {item_glossario("Paletização", "Agrupamento de mercadorias sobre paletes para facilitar a movimentação por empilhadeiras.")}
                {item_glossario("Giro de Estoque", "Indicador que mede quantas vezes o capital investido em estoque se renovou em um período.")}
                {item_glossario("Código EAN", "Código de barras universal (13 dígitos) para a unidade.")}
                {item_glossario("DUN (ou DUN-14)", "Código de barras (14 dígitos) para embalagens múltiplas/caixas.")}
            </div>
        """, unsafe_allow_html=True)

        # Técnicas e Métricas
        st.markdown(f"""
            <div class="glossary-card" style="margin-top: 15px;">
                <div class="glossary-category">📊 Técnicas & Métricas</div>
                {item_glossario("SPIN Selling", "Método de perguntas sobre Situação, Problema, Implicação e Necessidade.")}
                {item_glossario("Cross / Upselling", "Oferecer produtos complementares ou versões superiores.")}
                {item_glossario("Taxa de Conversão", "Percentual de leads ou contatos que realizam uma ação desejada (ex: fechar venda).")}
                {item_glossario("LTV (Lifetime Value)", "O valor financeiro total que um cliente traz durante o tempo que consome a marca.")}
                {item_glossario("Retenção", "A capacidade da empresa de manter os seus clientes ativos e fiéis.")}
                {item_glossario("NPS (Net Promoter Score)", "Métrica de lealdade que avalia a probabilidade de um cliente recomendar a empresa.")}
                {item_glossario("CSAT (Customer Satisfaction Score)", "Índice que mede o nível de satisfação do cliente com uma interação específica.")}
                {item_glossario("FCR (First Contact Resolution)", "Percentual de problemas resolvidos logo no primeiro contato com o suporte.")}
                {item_glossario("TMR / FRT (Tempo Médio de Resposta / First Response Time)", "Tempo médio que a equipe demora a dar a primeira resposta ao cliente.")}
                {item_glossario("TME (Tempo Médio de Espera)", "Tempo que o cliente passa a aguardar na fila antes de ser atendido.")}
                {item_glossario("TMA (Tempo Médio de Atendimento)", "Duração média total de cada atendimento ou interação com o cliente.")}
                {item_glossario("SLA (Service Level Agreement)", "Acordo que define prazos e níveis de qualidade prometidos no serviço.")}
                {item_glossario("CAC (Custo de Aquisição de Clientes)", "Investimento total em marketing e vendas dividido pelo número de novos clientes.")}
                
            </div>
        """, unsafe_allow_html=True)

        # Personagens de Vendas
        st.markdown(f"""
            <div class="glossary-card" style="margin-top: 15px;">
                <div class="glossary-category">🎭 Personagens de Vendas</div>
                {item_glossario("SDR (Sales Development Representative)", "Profissional que qualifica leads de entrada (Inbound) para a equipa de vendas.")}
                {item_glossario("BDR (Business Development Representative)", "Especialista em prospecção ativa e estratégica de novos mercados (Outbound).")}
                {item_glossario("Closer", "Vendedor responsável pelo fechamento final.")}
                {item_glossario("Farmer (Fazendeiro)", "Vendedor focado em cultivar e expandir a receita dentro da base de clientes que já existem.")}
                {item_glossario("CS (Customer Success)", "Gestor focado em garantir que o cliente alcance o sucesso e os resultados esperados com o produto.")}
            </div>
        """, unsafe_allow_html=True)
    
################################################################################
# --- MÓDULO 6: RESOLUÇÃO DE PROBLEMAS ---
################################################################################
elif aba_selecionada == "🛠️ Resolução de Problemas":
    st.header("🛠️ Resolução de Problemas")
    
    import base64
    import pytz
    from datetime import datetime
    from google.cloud import firestore
    from google.oauth2 import service_account

    # --- CONEXÃO COM O BANCO DE DADOS (FIRESTORE) ---
    if "db" not in st.session_state:
        try:
            creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
            st.session_state.db = firestore.Client(credentials=creds)
        except Exception as e:
            st.error(f"Erro de conexão com o banco: {e}")

    def carregar_dados_nuvem():
        try:
            docs = st.session_state.db.collection("ocorrencias").order_by("id_unico", direction=firestore.Query.DESCENDING).stream()
            return [doc.to_dict() for doc in docs]
        except Exception:
            return []

    def salvar_dados_nuvem(nova_nota):
        try:
            st.session_state.db.collection("ocorrencias").add(nova_nota)
            return True
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")
            return False

    if "historico_problemas" not in st.session_state:
        st.session_state.historico_problemas = carregar_dados_nuvem()

    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = 0

    # Layout em colunas: Esquerda (Guia de Soluções) | Direita (Registro e Histórico)
    col_conteudo, col_notas = st.columns([1.5, 1])

    with col_conteudo:
        st.subheader("📖 Guia de Tratativas Rápidas")
        st.write("Consulte como proceder em cada caso antes de registrar a ocorrência:")

        # Dicionário de dados extraído da sua planilha
        guia_problemas = {
            "📝 Processo de NFD (Devolução)": {
                "area": "LOGÍSTICA / FINANCEIRO",
                "responsavel": "RONALDO / MARCELLI",
                "contato": "logistica4@papapa.com.br; contasareceber2@papapa.com.br",
                "passo_a_passo": "1. **Validação:** Confirmar a ocorrência (avaria, validade ou erro de envio) com a Logística.\n2. **Emissão do Cliente:** O cliente deve emitir a Nota Fiscal de Devolução (NFD).\n3. **Requisito Obrigatório:** A NFD deve conter o número da **NF de origem** e o **motivo da devolução** descritos nas observações.\n4. **Financeiro:** Enviar a NFD para a Marcelli realizar o abatimento ou cancelamento do boleto."
             },
            "🚛 Prazo de Entrega / Atraso": {
                "area": "LOGÍSTICA",
                "responsavel": "RONALDO",
                "contato": "logistica4@papapa.com.br",
                "passo_a_passo": "Verificar no Follow Up e site da transportadora. Constatado o atraso, enviar solicitação à logística via formulário interno para entender o ocorrido e reportar ao cliente."
            },
            "📦 Avarias (Cargas molhadas/amassadas)": {
                "area": "LOGÍSTICA / FINANCEIRO",
                "responsavel": "RONALDO / MARCELLI",
                "contato": "logistica4@papapa.com.br; contasareceber2@papapa.com.br",
                "passo_a_passo": "1. Verificar ressalva no canhoto.\n2. Solicitar fotos das avarias.\n3. Se poucas unidades: propor bonificação ou desconto no próximo pedido (autorizar com João).\n4. Casos maiores: cliente formaliza por e-mail com NFD para logística/financeiro."
            },
            "🍎 Validade do Produto (< 60%)": {
                "area": "LOGÍSTICA / FINANCEIRO",
                "responsavel": "RONALDO / MARCELLI",
                "contato": "logistica4@papapa.com.br, contasareceber2@papapa.com.br",
                "passo_a_passo": "Solicitar lote e item ao cliente. Se confirmado erro interno, solicitar NFD ao cliente e solicitar abatimento no boleto ao financeiro."
            },
            "❌ Extravio de Mercadoria": {
                "area": "LOGÍSTICA / FINANCEIRO",
                "responsavel": "RONALDO / GABI / MARCELLI",
                "contato": "logistica4@papapa.com.br; operacoes@papapa.com.br; contasareceber2@papapa.com.br",
                "passo_a_passo": "Confirmado extravio: explicar ao cliente e oferecer novo envio com 5% de desconto (sob aprovação do João). Copiar Marcelli para cancelamento de boletos antigos."
            },
            "📄 Guia Retida no SEFAZ": {
                "area": "LOGÍSTICA",
                "responsavel": "RONALDO",
                "contato": "logistica4@papapa.com.br",
                "passo_a_passo": "Verificar se a guia foi enviada por e-mail. Caso retida, acionar o Ronaldo imediatamente para regularização."
            },
            "🍎 Problema de Qualidade / Produto": {
                "area": "QUALIDADE",
                "responsavel": "LORENA",
                "contato": "qualidade2@papapa.com.br",
                "passo_a_passo": "Ao receber reclamação sobre a integridade do produto (sabor, textura, embalagem com defeito, etc):\n\n"
                                 "1. **Coleta de Dados:** Solicitar ao cliente as informações abaixo.\n"
                                 "2. **Envio:** Encaminhar e-mail para a Lorena com os seguintes dados:\n\n"
                                 "   - **CNPJ do cliente:**\n"
                                 "   - **Lote do produto:**\n"
                                 "   - **Validade do produto:**\n"
                                 "   - **Quantidade afetada:**\n"
                                 "   - **Motivo principal:**\n"
                                 "   - **Data da compra (NF):**\n"
                                 "   - **E-mail do cliente:**\n"
                                 "   - **Telefone do cliente:**\n\n"
                                 "3. **Amostra:** Caso necessário, a Lorena solicitará o recolhimento da amostra para análise física."
            }
        }

        problema_selecionado = st.selectbox(
            "Selecione o tipo de problema:",
            list(guia_problemas.keys())
        )

        dados = guia_problemas[problema_selecionado]
        
        # Card de Solução Visual
        with st.container(border=True):
            st.markdown(f"### 🛠️ Solução: {problema_selecionado}")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**📍 Área:** {dados['area']}")
                st.markdown(f"**👤 Responsável:** {dados['responsavel']}")
            with c2:
                st.markdown(f"**📧 E-mail:** `{dados['contato']}`")
            
            st.markdown("---")
            st.markdown(f"**📝 Procedimento:**\n{dados['passo_a_passo']}")

    with col_notas:
        st.subheader("📝 Registro de Casos Críticos")

        def salvar_nota_callback():
            autor = st.session_state.get("nome_usuario_log")
            texto = st.session_state.get("input_area_problemas", "").strip()
            nf_pedido = st.session_state.get("input_nf_problema", "").strip()
            chave_atual = f"input_midia_prob_{st.session_state.uploader_key}"
            arquivos_anexos = st.session_state.get(chave_atual)
            
            if autor and texto:
                fuso_br = pytz.timezone('America/Sao_Paulo')
                agora = datetime.now(fuso_br)
                mes_ref = f"{['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'][agora.month - 1]}/2026"
                
                lista_arquivos = []
                if arquivos_anexos:
                    for arq in arquivos_anexos:
                        ext = arq.name.lower()
                        tipo = "video" if ext.endswith(('mp4', 'mov', 'avi')) else "foto"
                        b64 = base64.b64encode(arq.getvalue()).decode('utf-8')
                        lista_arquivos.append({"nome": arq.name, "bytes": b64, "tipo": tipo})
                
                nova_nota = {
                    "id_unico": agora.timestamp(),
                    "autor": autor,
                    "texto": texto,
                    "nf_pedido": nf_pedido,
                    "midias": lista_arquivos, 
                    "data": agora.strftime("%d/%m/%Y %H:%M"),
                    "mes_referencia": mes_ref
                }
                
                if salvar_dados_nuvem(nova_nota):
                    st.session_state.historico_problemas = carregar_dados_nuvem()
                    st.session_state["input_area_problemas"] = "" 
                    st.session_state["input_nf_problema"] = ""    
                    st.session_state.uploader_key += 1            
                    st.toast("✅ Registro salvo com sucesso!")
            else:
                st.error("Preencha Responsável e Descrição.")

        with st.expander("➕ Registrar Ocorrência", expanded=True):
            st.selectbox("Quem está registrando?", ["João Tadra", "Ana", "Pedro", "João Paulo", "Bernardo", "Thiago"], index=None, key="nome_usuario_log")
            st.text_input("Número da NF ou Pedido:", key="input_nf_problema")
            st.text_area("Descreva a ocorrência:", key="input_area_problemas", height=100)
            st.file_uploader("Anexar fotos/vídeos:", type=["png", "jpg", "jpeg", "mp4", "mov", "avi"], accept_multiple_files=True, key=f"input_midia_prob_{st.session_state.uploader_key}")
            st.button("Salvar Registro", use_container_width=True, on_click=salvar_nota_callback)

        st.write("---")
        st.subheader("📋 Histórico Recente")
        if st.session_state.historico_problemas:
            for nota in st.session_state.historico_problemas[:10]:
                with st.expander(f"📌 {nota.get('nf_pedido', 'S/ NF')} - {nota.get('autor')} ({nota.get('data')})"):
                    st.write(nota.get("texto"))
                    if nota.get("midias"):
                        cols_midia = st.columns(len(nota["midias"]))
                        for i, midia in enumerate(nota["midias"]):
                            with cols_midia[i]:
                                try:
                                    if midia["tipo"] == "foto":
                                        st.image(base64.b64decode(midia["bytes"]))
                                    else:
                                        st.video(base64.b64decode(midia["bytes"]))
                                except:
                                    st.warning("Mídia indisponível")
        else:
            st.write("Nenhuma ocorrência registrada.")

    st.divider()
                    
################################################################################
# --- MÓDULO 7: ARSENAL DE OBJEÇÕES ---
################################################################################
elif aba_selecionada == "🚫 Quebras de Excuses": 
    st.header("🚫 Arsenal de Objeções")
    
    # CSS para forçar a quebra de linha no st.code (evita a barra de rolagem lateral)
    st.markdown("""
        <style>
        code {
            white-space: pre-wrap !important;
            word-break: break-word !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("### 💡 Guia de Contorno Estratégico")
    st.caption("Clique na objeção e use o botão à direita para copiar o texto rapidamente.")

    # Dicionário atualizado com a nova objeção no topo (Total 11)
    objecoes = {
        "1. 🏪 Já tem muitas lojas vendendo Papapá (e mais barato)": "Entendo perfeitamente, isso mostra que a demanda pelo produto é real e o cliente já busca a marca. O segredo aqui não é brigar por preço, mas se diferenciar no PDV. Enquanto o grande mercado apenas 'empilha caixa', aqui você entrega uma venda consultiva, com atendimento técnico e especializado. Além disso, vocês podem trabalhar com kits personalizados (ex: kit introdução alimentar ou kit semana prática) que aumentam o seu ticket médio e tiram a comparação direta de preço unitário. O que você acha?",
        "2. 🤝 Já trabalho com outra marca de papinha": "Perfeito, isso é ótimo. Mostra que a categoria já performa aí dentro. A nossa proposta não é substituir, mas complementar e ampliar o ticket da categoria. Hoje vocês trabalham a curva completa ou existe espaço para uma marca com posicionamento mais premium e foco em recorrência?",
        "3. 📉 Não sei se tem giro para isso": "Faz sentido olhar com cautela. Por isso a entrada pode ser estratégica, com SKUs de maior giro e mix enxuto. A ideia não é aumentar risco de estoque, mas estruturar curva inteligente de produto. Posso te mostrar quais SKUs normalmente performam melhor nesse perfil de loja?",
        "4. 💰 Está caro comparado às marcas tradicionais": "Entendo a comparação. A diferença é que não competimos apenas por preço, mas por posicionamento e margem absoluta. Muitas vezes o produto premium gera maior rentabilidade por unidade e atrai um público que já está disposto a pagar mais por qualidade. Faz sentido analisarmos margem real por SKU?",
        "5. 🏢 Preciso falar com a central / diretoria": "Perfeito. Posso te apoiar com um resumo objetivo de potencial de giro, margem e proposta de mix inicial para facilitar essa validação interna. Se fizer sentido, também posso participar da apresentação para explicar rapidamente o racional da categoria.",
        "6. ⏳ Tenho medo de produto parado / vencimento": "Essa é uma preocupação legítima. Por isso trabalhamos com entrada estratégica e análise de giro. Além disso, ajudamos a definir mix ideal por perfil de loja. O objetivo não é inflar estoque, mas estruturar reposição inteligente.",
        "7. ⚠️ Já tive problema com fornecedor antes": "Entendo totalmente. O que normalmente gera problema é falta de acompanhamento e previsibilidade. Nossa proposta não é só vender produto, mas acompanhar giro e evolução de mix. Antes de avançar, posso entender o que aconteceu na experiência anterior para te mostrar como evitamos esse cenário?",
        "8. 📦 Não posso colocar muitos SKUs novos agora": "Perfeito. Podemos começar com 3 a 5 SKUs estratégicos de maior potencial e, conforme performance, evoluir o mix. A ideia é crescimento gradual e baseado em resultado, não entrada massiva.",
        "9. 🧐 Não vejo diferencial tão claro": "A principal diferença está na construção de categoria e recorrência. Não é apenas produto saudável, mas marca com posicionamento claro, proposta nutricional consistente e potencial de fidelização. Posso te mostrar como isso impacta recompra e ticket médio?",
        "10. 🗓️ Agora não é momento para novos fornecedores": "Entendo. Justamente por isso podemos começar pequeno, validando performance sem grande exposição. O objetivo não é gerar ruptura na operação, mas agregar incrementalmente.",
        "11. 🍼 Minha categoria infantil já está completa": "Excelente que você já olha para esse público. A Papapá entra justamente para captar o consumidor que busca o Clean Label (rótulo limpo), que hoje é a maior tendência de crescimento. Ter uma opção premium aumenta o ticket médio da sua categoria. Podemos testar o desempenho de 2 ou 3 itens específicos?"
    }

    # Exibição das 10 Objeções
    for titulo, texto in objecoes.items():
        with st.expander(titulo):
            st.code(texto, language=None)

    # --- DIVISOR ENTRE SEÇÕES ---
    st.markdown("---")
    
    # --- SEÇÃO PLUS: DIFERENCIAIS COMPETITIVOS ---
    st.markdown("### 🏆 Diferenciais Papapá (O seu 'Plus' nas vendas)")
    st.caption("Argumentos técnicos e comerciais para encantar o cliente.")

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("🍃 1. Comida de Verdade (Rótulo Limpo)"):
            texto_v1 = """Diferente das papinhas ultraprocessadas tradicionais, nossos produtos são 100% naturais:
• Zero adição de açúcar ou sal: Preserva o paladar do bebê.
• Sem conservantes ou corantes: A durabilidade vem da tecnologia de envase e esterilização, zero aditivos químicos."""
            st.code(texto_v1, language=None)

        with st.expander("👶 2. Tecnologia Pouch (Praticidade)"):
            texto_v2 = """Pioneiros no Brasil com embalagens flexíveis com bico:
• Práticas e Seguras: Estimula a autonomia do bebê (método similar ao BLW).
• Portáteis: Não precisam de refrigeração, perfeitas para viagens e passeios.
• Segurança: Embalagem multicamadas que protege contra luz e oxigênio, mantendo nutrientes."""
            st.code(texto_v2, language=None)

    with col2:
        with st.expander("🍎 3. Mix e Introdução Alimentar"):
            texto_v3 = """Variedade pensada na janela de oportunidades do bebê:
• Mix de Frutas e Legumes: Texturas e sabores variados.
• Papinhas Salgadas: Equilíbrio de proteínas, carboidratos e fibras.
• Snacks Saudáveis: Lanches que derretem na boca, ideais para a mastigação."""
            st.code(texto_v3, language=None)

        with st.expander("🤝 4. Rigor e Qualidade de Atendimento"):
            texto_v4 = """Compromisso logístico e comercial:
• Logística ágil para garantir produto fresco no PDV.
• Política de transparência e suporte total aos parceiros.
• Experiência positiva em todos os pontos de contato."""
            st.code(texto_v4, language=None)

    # Resumo Final
    with st.expander("✨ O Resumo: A essência da Papapá"):
        resumo_texto = "A Papapá é a aliada de quem não quer escolher entre a saúde do filho e a agitação da rotina moderna. É nutrição de alto nível com a conveniência que o mundo atual exige."
        st.code(resumo_texto, language=None)

    st.divider()
    st.success("**Dica de Ouro:** Transforme a objeção em uma oportunidade de educar o cliente sobre o valor da marca.")

################################################################################
# --- MÓDULO 8: 📈 IMPACTOS NO RESULTADO ---
################################################################################
elif aba_selecionada == "📈 Impactos no resultado":
    st.header("📈 Impactos no Resultado")
    
    import base64
    import pytz
    from datetime import datetime
    from google.cloud import firestore
    from google.oauth2 import service_account

    # --- CONEXÃO COM O BANCO (FIRESTORE) ---
    if "db" not in st.session_state:
        creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        st.session_state.db = firestore.Client(credentials=creds)

    def carregar_impactos_nuvem():
        try:
            docs = st.session_state.db.collection("impactos_v2").order_by("id_unico", direction=firestore.Query.DESCENDING).stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")
            return []

    def salvar_impacto_nuvem(novo_registro):
        try:
            st.session_state.db.collection("impactos_v2").add(novo_registro)
            return True
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")
            return False

    if "historico_impactos" not in st.session_state:
        st.session_state.historico_impactos = carregar_impactos_nuvem()

    if "uploader_impacto_key" not in st.session_state:
        st.session_state.uploader_impacto_key = 200

    col_info, col_form = st.columns([1, 1.2])

    with col_info:
        st.subheader("O que registramos aqui?")
        st.write("""
        Nesta seção, o time deve registrar ações ou eventos que alteraram os indicadores (positiva ou negativamente).
        - **Exemplo Positivo:** Nova estratégia de abordagem que subiu o ticket médio.
        - **Exemplo Negativo:** Ruptura de estoque que impediu a batida da meta.
        """)
        st.image("https://img.freepik.com/free-vector/growth-arrow-concept-illustration_114360-1090.jpg", width=300)

    with col_form:
        st.subheader("🚀 Novo Registro de Impacto")

        def salvar_impacto_callback():
            autor = st.session_state.get("imp_autor")
            tipo = st.session_state.get("imp_tipo")
            descricao = st.session_state.get("imp_desc", "").strip()
            valor = st.session_state.get("imp_valor", 0.0)
            doc_cliente = st.session_state.get("imp_doc", "").strip()
            
            chave_u = f"midia_imp_{st.session_state.uploader_impacto_key}"
            arquivos = st.session_state.get(chave_u)
            
            if autor and tipo and descricao:
                fuso_br = pytz.timezone('America/Sao_Paulo')
                agora = datetime.now(fuso_br)
                mes_ref = f"{['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'][agora.month - 1]}/2026"

                lista_midias = []
                if arquivos:
                    for arq in arquivos:
                        ext = arq.name.lower()
                        tipo_m = "video" if ext.endswith(('mp4','mov','avi')) else "audio" if ext.endswith(('mp3','wav','ogg')) else "foto"
                        b64 = base64.b64encode(arq.getvalue()).decode('utf-8')
                        lista_midias.append({"nome": arq.name, "bytes": b64, "tipo": tipo_m})

                novo_item = {
                    "id_unico": agora.timestamp(),
                    "autor": autor,
                    "tipo": tipo,
                    "valor_impacto": valor,
                    "documento": doc_cliente,
                    "descricao": descricao,
                    "midias": lista_midias,
                    "data": agora.strftime("%d/%m/%Y %H:%M"),
                    "mes_referencia": mes_ref
                }
                
                if salvar_impacto_nuvem(novo_item):
                    st.session_state.historico_impactos = carregar_impactos_nuvem()
                    st.session_state["imp_desc"] = ""
                    st.session_state["imp_doc"] = ""
                    st.session_state["imp_valor"] = 0.0
                    st.session_state.uploader_impacto_key += 1
                    st.toast("✅ Impacto registrado com sucesso!")
            else:
                st.error("Preencha Responsável, Tipo e Descrição.")

        with st.expander("📝 Abrir Formulário", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                st.selectbox("Responsável:", ["João Tadra", "Ana", "Pedro", "João Paulo", "Bernardo", "Thiago"], index=None, key="imp_autor")
                st.radio("Tipo do Impacto:", ["🟢 Positivo", "🔴 Negativo"], key="imp_tipo", horizontal=True)
            with c2:
                st.text_input("NF / Pedido / CNPJ:", placeholder="Identificação...", key="imp_doc")
                st.number_input("Estimativa de Valor (R$):", min_value=0.0, step=100.0, key="imp_valor")
            
            st.text_area("Descrição do ocorrido:", placeholder="Explique o impacto no resultado...", key="imp_desc")
            st.file_uploader("Anexar Provas:", type=["png","jpg","jpeg","mp4","mov","avi","mp3","wav"], accept_multiple_files=True, key=f"midia_imp_{st.session_state.uploader_impacto_key}")
            st.button("Salvar Impacto no Resultado", use_container_width=True, on_click=salvar_impacto_callback)

    st.divider()

    # --- FILTROS DE CONSULTA (Garantindo que as variáveis existam antes de usar) ---
    st.subheader("🔍 Filtros de Consulta")
    f_c1, f_c2 = st.columns(2)
    with f_c1:
        meses_lista = ["Todos"] + [f"{m}/2026" for m in ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]]
        filtro_mes = st.selectbox("Filtrar por Mês:", meses_lista)
    with f_c2:
        filtro_tipo = st.multiselect("Filtrar por Tipo:", ["🟢 Positivo", "🔴 Negativo"])

    # --- PROCESSAMENTO DOS DADOS FILTRADOS ---
    dados_exibidos = st.session_state.historico_impactos
    
    if filtro_mes != "Todos":
        dados_exibidos = [d for d in dados_exibidos if d.get('mes_referencia') == filtro_mes]
    
    if filtro_tipo:
        dados_exibidos = [d for d in dados_exibidos if d.get('tipo') in filtro_tipo]

    # --- CÁLCULO DOS TOTAIS FINANCEIROS ---
    total_positivo = sum(d.get('valor_impacto', 0.0) for d in dados_exibidos if d.get('tipo') == "🟢 Positivo")
    total_negativo = sum(d.get('valor_impacto', 0.0) for d in dados_exibidos if d.get('tipo') == "🔴 Negativo")

    # --- EXIBIÇÃO DAS MÉTRICAS ---
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Ocorrências", len(dados_exibidos))
    with m2:
        st.metric("Total Positivo", f"R$ {total_positivo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    with m3:
        st.metric("Total Negativo", f"R$ {total_negativo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), delta_color="inverse")

    st.divider()

    # --- LISTAGEM ---
    for idx, item in enumerate(dados_exibidos):
        with st.container():
            c_info, c_del = st.columns([0.9, 0.1])
            with c_info:
                st.markdown(f"### {item.get('tipo')} - R$ {item.get('valor_impacto', 0):,.2f}")
                st.caption(f"📅 {item.get('data')} | 📂 {item.get('mes_referencia')} | 👤 {item.get('autor')}")
                if item.get('documento'): st.markdown(f"**📄 Ref:** `{item.get('documento')}`")
                st.info(item.get("descricao"))
                
                midias = item.get("midias", [])
                if midias:
                    m_cols = st.columns(len(midias) if len(midias) < 5 else 5)
                    for i, m in enumerate(midias):
                        with m_cols[i % 5]:
                            icon = "🖼️" if m["tipo"] == "foto" else "🎥" if m["tipo"] == "video" else "🎵"
                            with st.popover(f"{icon} Ver", use_container_width=True):
                                b_data = base64.b64decode(m["bytes"])
                                if m["tipo"] == "video": st.video(b_data)
                                elif m["tipo"] == "audio": st.audio(b_data)
                                else: st.image(b_data, use_container_width=True)
            
            with c_del:
                if st.button("🗑️", key=f"del_imp_v2_{item.get('id_unico')}"):
                    docs = st.session_state.db.collection("impactos_v2").where("id_unico", "==", item.get("id_unico")).stream()
                    for doc in docs: doc.reference.delete()
                    st.session_state.historico_impactos = carregar_impactos_nuvem()
                    st.rerun()
            st.markdown("<hr style='margin:10px 0; opacity:0.2'>", unsafe_allow_html=True)
    
################################################################################
# --- MÓDULO 9: LINKS ÚTEIS ---
################################################################################
elif aba_selecionada == "🔗 Links Úteis":
    st.title("🔗 Central de Links Úteis")
    st.write("Acesse rapidamente as ferramentas e formulários da nossa operação.")
    
    # --- BLOCO ATUALIZADO: FERRAMENTAS DE TRABALHO (3 COLUNAS) ---
    with st.container():
        st.subheader("🛠️ Ferramentas de Trabalho - Inside Sales")
        col_v1, col_v2, col_v3 = st.columns(3)
        with col_v1:
            st.link_button("📦 Dibb (ERP)", "http://170.231.15.12:8080/web/view/app/ger/GER801V.php?term=3321245", use_container_width=True)
            st.caption("Consulta de pedidos e faturamento")
        with col_v2:
            st.link_button("🚀 RD CRM (Pipeline)", "https://crm.rdstation.com/app/deals/pipeline", use_container_width=True)
            st.caption("Gestão de funil e negociações")
        with col_v3:
            st.link_button("🤖 Vekta AI", "https://app.vektasales.com.br/chat", use_container_width=True)
            st.caption("Nossa ferramenta de Inteligência Artificial")
    
    st.markdown("---")

    with st.container():
        st.subheader("📝 Cadastros - Inside Sales")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.link_button("📄 Forms Cadastro", "https://forms.office.com/pages/responsepage.aspx?id=KcXm9q-wZUOFUmPbM0a-aQ0xpHiomcxDhUissuWVgb9UMVU4UzNNWkc1REM3Vlk0SzVQMlZLSU5BWS4u&route=shorturl", use_container_width=True)
            st.caption("Novo cadastro e atualização de clientes")
        with col2:
            st.link_button("👀 Acompanhar Cadastros", "https://papapacombr-my.sharepoint.com/:x:/g/personal/cadastros_papapa_com_br/IQDkMQgW0iAgTqw7aetudCfXAeVaoV7m17dbUSH7QNGzkv0?e=hQu864", use_container_width=True)
            st.caption("Acompanhamento da realização dos cadastros")
        with col3:
            st.link_button("🔍 Consultar CENPROT", "https://www.pesquisaprotesto.com.br/", use_container_width=True)
            st.caption("Verificar protestos de CNPJs antes do pedido")
        with col4:
            st.link_button("🌐 Consultar SINTEGRA", "http://www.sintegra.gov.br/", use_container_width=True)
            st.caption("Verificar a situação cadastral e IE do CNPJ")
            
        

    st.markdown("---")

    with st.container():
        st.subheader("📝 Cadastros - Regionais e RCA")
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("📄 Forms Cadastro", "https://statics.teams.cdn.office.net/evergreen-assets/safelinks/2/atp-safelinks.html", use_container_width=True)
            st.caption("Novo cadastro e atualização de clientes")
        with col2:
            st.link_button("👀 Acompanhar Cadastros", "https://docs.google.com/spreadsheets/d/1KrwiEVyjguz8cPjnHsOM2ymbcP5aB2AfhTQczppvtpc/edit?gid=1200882492#gid=1200882492", use_container_width=True)
            st.caption("Acompanhamento da realização dos cadastros")

    st.markdown("---")

    with st.container():
        st.subheader("🗂️ Fichas Comerciais")
        st.link_button("📂 Fichas comerciais de produtos", "https://papapacombr.sharepoint.com/sites/Papapa-Fileserver/Documentos%20Compartilhados/Forms/AllItems.aspx?id=%2Fsites%2FPapapa%2DFileserver%2FDocumentos%20Compartilhados%2FComercial%2F0%20%2D%20COMERCIAL%2F10%20%2D%20Ficha%20cadastral%20de%20produtos&p=true&ct=1776191232287&or=Teams%2DHL&ga=1&LOF=1", use_container_width=True)
        st.caption("Fichas comerciais de produtos")

    st.markdown("---")

    with st.container():
        st.subheader("🛍️ Pedidos de bonificação")
        st.link_button("✍️ Pedidos de bonificação", "https://docs.google.com/forms/d/1IwICqg6apNUdhyQAX9vQHO6zKggJACffmynCMDvVrg4/viewform?edit_requested=true", use_container_width=True)
        st.caption("Formulário para pedidos de bonificação")

    st.markdown("---")
    
    with st.container():
        st.subheader("📊 Dashboard - Inside Sales")
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
    t1, t2, t3, t4 = st.columns(4) # Alterado para 4 colunas
    
    with t1:
        st.markdown("**Translovato**")
        st.link_button("Rastrear Lovato", "https://www.translovato.com.br/portal/rastreamento", use_container_width=True)
        st.code("User: BABY\nPass: Papapa@2026")
        
    with t2:
        st.markdown("**Tecmar**")
        st.link_button("Portal Tecmar", "https://smonet.tecmartransportes.com.br/smonet/#/notas-fiscais", use_container_width=True)
        st.code("User: babyroo\nPass: babyroo1*")
        
    with t3:
        st.markdown("**Rodovitor**")
        st.link_button("Rastrear Rodovitor", "https://ssw.inf.br/2/rastreamento", use_container_width=True)
        st.caption("Acesso via SSW")

    with t4: # Nova coluna para Rodonaves
        st.markdown("**Rodonaves**")
        st.link_button("Portal Rodonaves", "https://rodonaves.com.br/rastreio-de-mercadoria", use_container_width=True)
        st.caption("Rastreio via CNPJ/NF")

    st.markdown("---")

    st.subheader("🎨 Marketing e Divulgação")
    st.markdown("##### Compartilhe com o cliente para fotos, logos, fichas cadastrais e materiais de PDV.")
    
    # --- Linha do Link Novo ---
    c1, c2 = st.columns([1, 2])
    with c1:
        st.link_button(
            "📂 Drive para Lojistas (Novo)", 
            "https://drive.google.com/drive/folders/137gBnZp7qFkDnQRTNyMfsBH4kO59XwTC", 
            use_container_width=True,
            type="primary"
        )
    with c2:
        # Usamos markdown com um leve ajuste para centralizar verticalmente com o botão
        st.info("💡 O **link novo** possui acesso livre.")

    # --- Linha do Link Antigo ---
    c3, c4 = st.columns([1, 2])
    with c3:
        st.link_button(
            "📂 Drive para Lojistas (Antigo)", 
            "https://papapacombr-my.sharepoint.com/:f:/g/personal/bi_papapa_com_br/EkwEgijW7pNCm95ElhfbiHoBK4kVtHiWieDpIOmwFZwRgA", 
            use_container_width=True
        )
    with c4:
        st.warning("**Senha do link antigo:** Papapa@2023")

import streamlit as st
import pandas as pd

import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

################################################################################
# --- MÓDULO 10: SIMULADOR DE PEDIDOS (CONFIGURAÇÕES) ---
################################################################################

import os
from pathlib import Path
import unicodedata
import pandas as pd
import streamlit as st
from fpdf import FPDF

VERSAO_TABELAS = "2026-06-03-01"

mapa_tabelas = {
    "Selecione uma tabela": None,
    "ESPECIAL": "ESPECIAL_reajuste abril26 - Era uma vez.xlsx",
    "ESPECIAL REDE (-10%)": "ESPECIAL REDE (-10)_reajuste abril26 - Era uma vez.xlsx",
    "FARMA 0": "0325FARMA + ESPECIAL_PC Era uma vez.xlsx",
    "FARMA V": "0325FARMA + ESPECIAL_v_PC Era uma vez.xlsx",
    "FARMA X": "0325FARMA + ESPECIAL_x_PC Era uma vez.xlsx",
    "CASH AND CARRY 0": "0325C_PC reajuste abril26 - Era uma Vez.xlsx",
    "CASH AND CARRY V": "0325Cv_PC reajuste abril26 - Era uma Vez.xlsx",
    "DISTRIBUIDOR 0": "0325D_PC reajuste abril26 - Era uma Vez.xlsx",
    "DISTRIBUIDOR V": "0325Dv_PC reajuste abril26 - Era uma Vez.xlsx",
    "DISTRIBUIDOR X": "0325Dx_PC reajuste abril26 - Era uma Vez.xlsx",
    "VAREJO 0": "0325V_PC reajuste abril26 - Era uma vez.xlsx",
    "VAREJO V": "0325Vv_PC reajustes abril26 - Era uma Vez.xlsx",
    "VAREJO X": "0325Vx_PC reajuste abril26 - Era uma Vez.xlsx"
}

def texto_normalizado(valor):
    txt = str(valor).strip().lower()
    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(ch for ch in txt if not unicodedata.combining(ch))
    txt = txt.replace("\n", " ")
    txt = txt.replace("-", " ")
    txt = txt.replace("_", " ")
    txt = txt.replace("(", " ")
    txt = txt.replace(")", " ")
    txt = txt.replace("%", " ")
    txt = " ".join(txt.split())
    return txt

def nome_indica_especial_rede_10(nome_arquivo):
    nome = texto_normalizado(nome_arquivo)
    return "especial" in nome and "rede" in nome and "10" in nome

def localizar_arquivo_tabela(arquivo, tabela_sel=None, mostrar_erro=True):
    if not arquivo:
        return None

    pasta_app = Path(__file__).parent
    nome_arquivo = Path(arquivo).name
    nome_norm = texto_normalizado(nome_arquivo)

    exige_rede_10 = tabela_sel == "ESPECIAL REDE (-10%)"
    bloqueia_rede_10 = tabela_sel == "ESPECIAL"

    def arquivo_valido(caminho):
        if exige_rede_10 and not nome_indica_especial_rede_10(caminho.name):
            return False

        if bloqueia_rede_10 and nome_indica_especial_rede_10(caminho.name):
            return False

        return True

    caminhos_possiveis = [
        pasta_app / arquivo,
        pasta_app / nome_arquivo,
        pasta_app / "tabelas" / arquivo,
        pasta_app / "tabelas" / nome_arquivo,
        pasta_app / "ESPECIAL" / nome_arquivo,
        pasta_app / "tabelas" / "ESPECIAL" / nome_arquivo,
        pasta_app / "data" / nome_arquivo,
        pasta_app / "dados" / nome_arquivo,
    ]

    for caminho in caminhos_possiveis:
        if caminho.exists() and arquivo_valido(caminho):
            return caminho.resolve()

    todos_arquivos = [p for p in pasta_app.rglob("*.xlsx") if p.is_file()]

    equivalentes = []
    for caminho in todos_arquivos:
        if texto_normalizado(caminho.name) == nome_norm and arquivo_valido(caminho):
            equivalentes.append(caminho.resolve())

    if equivalentes:
        return sorted(equivalentes, key=lambda p: len(str(p)))[0]

    palavras = [
        p for p in nome_norm.replace("xlsx", "").split()
        if p not in ["nao", "não", "usar"]
    ]

    candidatos = []
    for caminho in todos_arquivos:
        nome_candidato = texto_normalizado(caminho.name)

        if not arquivo_valido(caminho):
            continue

        if all(palavra in nome_candidato for palavra in palavras[:5]):
            candidatos.append(caminho.resolve())

    if candidatos:
        return sorted(candidatos, key=lambda p: len(str(p)))[0]

    if mostrar_erro:
        st.error(f"Arquivo correto não encontrado para {tabela_sel}: {nome_arquivo}")

    return None

def carregar_dados_completos_por_caminho(caminho_arquivo):
    if not caminho_arquivo:
        return None, {}, None

    try:
        caminho_arquivo = Path(caminho_arquivo)

        df_p = pd.read_excel(caminho_arquivo, sheet_name="PREÇOS", header=1)
        df_p.columns = df_p.columns.astype(str).str.strip()

        if "Estado" in df_p.columns:
            df_p["Estado"] = df_p["Estado"].astype(str).str.strip()

        try:
            df_tabelas = pd.read_excel(caminho_arquivo, sheet_name="Tabelas", header=None)
        except Exception:
            df_tabelas = None

        st_dict = {}
        xl = pd.ExcelFile(caminho_arquivo)

        for sheet in xl.sheet_names:
            if str(sheet).startswith("ST "):
                df_st = pd.read_excel(xl, sheet_name=sheet)
                df_st.columns = df_st.columns.astype(str).str.strip()

                if "Estado" in df_st.columns:
                    df_st["Estado"] = df_st["Estado"].astype(str).str.strip()

                st_dict[sheet] = df_st

        return df_p, st_dict, df_tabelas

    except Exception as e:
        st.error(f"Erro ao carregar arquivo de tabelas/ST: {e}")
        return None, {}, None

def moeda_br(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def valor_float(valor):
    if pd.isna(valor):
        return 0.0

    if isinstance(valor, (int, float)):
        return float(valor)

    txt = str(valor).replace("R$", "").strip()

    if txt in ["", "-", "nan", "None"]:
        return 0.0

    txt = txt.replace(" ", "")

    if "," in txt and "." in txt:
        txt = txt.replace(".", "").replace(",", ".")
    elif "," in txt:
        txt = txt.replace(",", ".")

    try:
        return float(txt)
    except Exception:
        return 0.0

def buscar_valor_linha(df, estado, coluna):
    if df is None or coluna not in df.columns or "Estado" not in df.columns:
        return 0.0

    linha = df[df["Estado"].astype(str).str.strip() == estado]

    if linha.empty:
        return 0.0

    return valor_float(linha[coluna].values[0])

def buscar_linha_cabecalho_tabelas(df_tabelas, linha_produto_idx):
    if df_tabelas is None:
        return None

    inicio = max(0, linha_produto_idx - 30)

    for r in range(linha_produto_idx - 1, inicio - 1, -1):
        textos = [texto_normalizado(df_tabelas.iat[r, c]) for c in range(df_tabelas.shape[1])]
        tem_descricao = any("descricao" in txt for txt in textos)
        tem_valor_unit = any("valor unit" in txt for txt in textos)

        if tem_descricao and tem_valor_unit:
            return r

    return None

def buscar_coluna_por_header(df_tabelas, linha_header, termos_obrigatorios, termos_proibidos=None):
    if df_tabelas is None or linha_header is None:
        return None

    termos_proibidos = termos_proibidos or []

    for c in range(df_tabelas.shape[1]):
        txt = texto_normalizado(df_tabelas.iat[linha_header, c])

        if all(termo in txt for termo in termos_obrigatorios) and not any(termo in txt for termo in termos_proibidos):
            return c

    return None

def buscar_item_na_aba_tabelas(df_tabelas, nome_produto):
    if df_tabelas is None:
        return None

    nome_busca = texto_normalizado(nome_produto)

    for r in range(df_tabelas.shape[0]):
        for c in range(df_tabelas.shape[1]):
            descricao = texto_normalizado(df_tabelas.iat[r, c])

            if descricao == nome_busca:
                linha_header = buscar_linha_cabecalho_tabelas(df_tabelas, r)

                col_valor_unit = buscar_coluna_por_header(
                    df_tabelas,
                    linha_header,
                    ["valor", "unit"],
                    ["caixa", "total"]
                )
                col_st_un = buscar_coluna_por_header(
                    df_tabelas,
                    linha_header,
                    ["substituicao", "tributaria"]
                )
                col_ipi = buscar_coluna_por_header(
                    df_tabelas,
                    linha_header,
                    ["ipi"]
                )

                if col_valor_unit is None:
                    col_valor_unit = c + 10
                if col_st_un is None:
                    col_st_un = c + 12
                if col_ipi is None:
                    col_ipi = c + 13

                preco_unit = valor_float(df_tabelas.iat[r, col_valor_unit]) if col_valor_unit < df_tabelas.shape[1] else 0.0
                st_unit = valor_float(df_tabelas.iat[r, col_st_un]) if col_st_un < df_tabelas.shape[1] else 0.0
                ipi_unit = valor_float(df_tabelas.iat[r, col_ipi]) if col_ipi < df_tabelas.shape[1] else 0.0

                if preco_unit > 1000:
                    preco_unit = 0.0

                return {
                    "preco_unit": preco_unit,
                    "st_unit": st_unit,
                    "ipi_unit": ipi_unit,
                }

    return None

def coluna_nova_linha(coluna):
    return coluna in [
        "Salgadinhos",
        "Bisc. Recheados",
        "Sucos",
        "Achocolatado",
        "Puer. Talheres",
        "Puer. Babador",
        "Puer. Bolw",
        "Puer. Pratinho",
    ]

def produto_recebe_desconto_rede(config):
    # Na ESPECIAL REDE (-10%), o desconto de 10% vale apenas para PAPAPÁ.
    # ERA UMA VEZ e PUERICULTURA não recebem esse desconto.
    return not coluna_nova_linha(config["coluna"])

def calcular_valores_produto(
    df_precos,
    df_tabelas,
    dicionario_st,
    estado,
    regime_simples,
    nome_produto,
    config,
    fator_preco=1.0
):
    col_planilha = config["coluna"]
    un_cx = config["un_cx"]

    fator_do_produto = fator_preco

    if fator_preco != 1.0 and not produto_recebe_desconto_rede(config):
        fator_do_produto = 1.0

    if df_precos is not None and col_planilha in df_precos.columns:
        preco_unit = buscar_valor_linha(df_precos, estado, col_planilha) * fator_do_produto
        valor_cx_base = preco_unit * un_cx

        st_unitario = 0.0
        aba_st_alvo = config["aba_st"]

        if aba_st_alvo and aba_st_alvo in dicionario_st:
            coluna_st_tipo = "ST Simples" if regime_simples == "SIM" else "ST Normal"
            st_unitario = buscar_valor_linha(dicionario_st[aba_st_alvo], estado, coluna_st_tipo)

        ipi_cx = valor_cx_base * config.get("ipi", 0.0)
        st_cx = st_unitario * un_cx
        valor_caixa_total = valor_cx_base + st_cx + ipi_cx

        return preco_unit, st_unitario, ipi_cx, valor_caixa_total

    item_tabelas = buscar_item_na_aba_tabelas(df_tabelas, nome_produto)

    if item_tabelas:
        preco_unit = item_tabelas["preco_unit"] * fator_do_produto
        st_unitario = item_tabelas["st_unit"]
        ipi_unitario = item_tabelas["ipi_unit"]

        ipi_cx = ipi_unitario * un_cx
        valor_caixa_total = (preco_unit + st_unitario + ipi_unitario) * un_cx

        return preco_unit, st_unitario, ipi_cx, valor_caixa_total

    return 0.0, 0.0, 0.0, 0.0

categorias_produtos = {
    "PAPAPÁ": {
        "PAPINHA DE CARNE": {
            "Papinha Papapa Carne Arroz Legumes 120g": {"coluna": "Pouch Carne", "aba_st": None, "un_cx": 12, "cod": "5313", "ipi": 0.0},
            "Papinha Papapa Frango Grão Vegetais 120g": {"coluna": "Pouch Carne", "aba_st": None, "un_cx": 12, "cod": "5320", "ipi": 0.0},
        },
        "YOGUZINHO": {
            "Papinha Papapa Iogurte Frutas Amarelas e Banana 100g": {"coluna": "Yoguzinho", "aba_st": "ST PAPAPASTA", "un_cx": 16, "cod": "5566", "ipi": 0.0},
            "Papinha Papapa Iogurte Frutas Vermelhas e Banana 100g": {"coluna": "Yoguzinho", "aba_st": "ST PAPAPASTA", "un_cx": 16, "cod": "5573", "ipi": 0.0},
        },
        "PAPINHA DE FRUTA": {
            "Papinha Papapá Org Maçã Ameixa 100g": {"coluna": "Papinhas", "aba_st": "ST PAPAPASTA", "un_cx": 12, "cod": "17898994908729", "ipi": 0.0},
            "Papinha Papapá Org Banana Mirtilo Quinoa 100g": {"coluna": "Papinhas", "aba_st": "ST PAPAPASTA", "un_cx": 12, "cod": "17898994908736", "ipi": 0.0},
            "Papinha Papapá Org Manga 100g": {"coluna": "Papinhas", "aba_st": "ST PAPAPASTA", "un_cx": 12, "cod": "17898994908712", "ipi": 0.0},
            "Papinha Papapá Org Pera Espinafre Abobrinha 100g": {"coluna": "Papinhas", "aba_st": "ST PAPAPASTA", "un_cx": 12, "cod": "17898994908750", "ipi": 0.0},
            "Papinha Papapá Org Maçã B. Doce Cenoura 100g": {"coluna": "Papinhas", "aba_st": "ST PAPAPASTA", "un_cx": 12, "cod": "27898994908757", "ipi": 0.0},
            "Papinha Papapá Org Morango Maçã 100g": {"coluna": "Papinhas", "aba_st": "ST PAPAPASTA", "un_cx": 12, "cod": "5306", "ipi": 0.0},
        },
        "PALITINHO": {
            "Biscoito inf Papapá org. Beterraba 20g": {"coluna": "Palitinhos", "aba_st": "ST PALITINHOS", "un_cx": 16, "cod": "5085", "ipi": 0.0},
            "Biscoito inf Papapá org. Cenoura 20g": {"coluna": "Palitinhos", "aba_st": "ST PALITINHOS", "un_cx": 16, "cod": "5078", "ipi": 0.0},
            "Biscoito inf Papapá org. Tomate/Manjericão 20g": {"coluna": "Palitinhos", "aba_st": "ST PALITINHOS", "un_cx": 16, "cod": "5061", "ipi": 0.0},
        },
        "DENTIÇÃO": {
            "Biscoito Inf Papapá dent. Maçã e Abóbora 36g": {"coluna": "Biscoitinhos", "aba_st": "ST BISCOITINHOS", "un_cx": 12, "cod": "8774", "ipi": 0.0},
            "Biscoito Inf Papapá dent Vegetais 36g": {"coluna": "Biscoitinhos", "aba_st": "ST BISCOITINHOS", "un_cx": 12, "cod": "8767", "ipi": 0.0},
        },
        "MACARRÃO": {
            "Macarrao Inf Papapá m. Elbow Quinoa 200g": {"coluna": "Papapasta", "aba_st": "ST PAPAPASTA", "un_cx": 12, "cod": "5290", "ipi": 0.0},
            "Macarrao Inf Papapá m. Fusilli Vegetais 200g": {"coluna": "Papapasta", "aba_st": "ST PAPAPASTA", "un_cx": 12, "cod": "5283", "ipi": 0.0},
        },
        "LA CHEF": {
            "Sopinha Papapá org Lentinha Carne Legumes 180g": {"coluna": "La Chef", "aba_st": "ST PAPAPASTA", "un_cx": 6, "cod": "5276", "ipi": 0.0},
            "Risotinho Papapá org Arroz quinoa frango 180g": {"coluna": "La Chef", "aba_st": "ST PAPAPASTA", "un_cx": 6, "cod": "5269", "ipi": 0.0},
            "Caseirinho Papapá org Arroz feijão carne leg. 180g": {"coluna": "La Chef", "aba_st": "ST PAPAPASTA", "un_cx": 6, "cod": "5252", "ipi": 0.0},
        },
        "CEREAL": {
            "Cereal Infantil Papapá Aveia - Morango e Beterraba sache 170g": {"coluna": "P. Cereal 170g Sache sabores", "aba_st": "ST CEREAL SABOR POUCH 170", "un_cx": 12, "cod": "5402", "ipi": 0.0},
            "Cereal Infantil Papapá Aveia - Banana e Ameixa sache 170g": {"coluna": "P. Cereal 170g Sache sabores", "aba_st": "ST CEREAL SABOR POUCH 170", "un_cx": 12, "cod": "5419", "ipi": 0.0},
            "Cereal Infantil Papapá Aveia - Multicereais sache 170g": {"coluna": "P. Cereal 170g Sache MULTI", "aba_st": "ST MULTI 170 POUCH", "un_cx": 12, "cod": "5429", "ipi": 0.0},
            "Cereal Infantil Papapá Aveia - Multicereais sache 500g": {"coluna": "MULTI sache 500 g", "aba_st": "ST MULTI 500 POUCH", "un_cx": 12, "cod": "5399", "ipi": 0.0},
        },
        "BISCOTTI": {
            "Biscoito Infantil Papapá Biscotti com Laranja e Cenoura 60g": {"coluna": "Biscotti", "aba_st": "ST BISCOTTI", "un_cx": 12, "cod": "5375", "ipi": 0.0},
            "Biscoito Infantil Papapá Biscotti com Maçã e Canela 60g": {"coluna": "Biscotti", "aba_st": "ST BISCOTTI", "un_cx": 12, "cod": "5351", "ipi": 0.0},
            "Biscoito Infantil Papapá Biscotti com Banana e Cacau 60g": {"coluna": "Biscotti", "aba_st": "ST BISCOTTI", "un_cx": 12, "cod": "5368", "ipi": 0.0},
            "Biscoito Infantil Papapá Biscotti Goiaba 60g": {"coluna": "Biscotti", "aba_st": "ST BISCOTTI", "un_cx": 12, "cod": "5597", "ipi": 0.0},
            "Biscoito Infantil Papapá Biscotti com Maracujá e Camomila 60g": {"coluna": "Biscotti", "aba_st": "ST BISCOTTI", "un_cx": 12, "cod": "5580", "ipi": 0.0},
        },
        "SOPINHA": {
            "Sopinha Papapá Frango Arroz Legumes 240g (2x 120g)": {"coluna": "Bowl", "aba_st": None, "un_cx": 6, "cod": "5610", "ipi": 0.0},
            "Sopinha Papapá Carne Macarrao Legumes 240g (2x 120g)": {"coluna": "Bowl", "aba_st": None, "un_cx": 6, "cod": "5634", "ipi": 0.0},
            "Sopinha Papapá Carne Mandioq Leg 240g (2x 120g)": {"coluna": "Bowl", "aba_st": None, "un_cx": 6, "cod": "5627", "ipi": 0.0},
            "Sopinha Papapá Feijão Carne Leg 240g (2x 120g)": {"coluna": "Bowl", "aba_st": None, "un_cx": 6, "cod": "5606", "ipi": 0.0},
        }
    },
    "ERA UMA VEZ": {
        "SALGADINHOS": {
            "Salgadinho Integral Orgânico Queijo Papapa Era Uma Vez 40g": {"coluna": "Salgadinhos", "aba_st": "ST EXTRUSADOS", "un_cx": 18, "cod": "5670", "ipi": 0.0},
            "Salgadinho Integral Orgânico Cebola & Salsa Papapa Era Uma Vez 40g": {"coluna": "Salgadinhos", "aba_st": "ST EXTRUSADOS", "un_cx": 18, "cod": "5671", "ipi": 0.0},
            "Salgadinho Integral Orgânico Churrasco Papapa Era Uma Vez 40g": {"coluna": "Salgadinhos", "aba_st": "ST EXTRUSADOS", "un_cx": 18, "cod": "5673", "ipi": 0.0},
        },
        "BISCOITO RECHEADO": {
            "Biscoito Recheado de Frutas Amarelas Papapa Era Uma Vez 30g": {"coluna": "Bisc. Recheados", "aba_st": "ST RECHEADOS", "un_cx": 8, "cod": "5677", "ipi": 0.0},
            "Biscoito Recheado de Morango Papapa Era Uma Vez 30g": {"coluna": "Bisc. Recheados", "aba_st": "ST RECHEADOS", "un_cx": 8, "cod": "5678", "ipi": 0.0},
        },
        "SUCOS": {
            "Bebida de Laranja Papapa Era Uma Vez 200ml": {"coluna": "Sucos", "aba_st": None, "un_cx": 27, "cod": "5680", "ipi": 0.0},
            "Bebida de Uva Papapa Era Uma Vez 200ml": {"coluna": "Sucos", "aba_st": None, "un_cx": 27, "cod": "5681", "ipi": 0.0},
            "Bebida de Morango Papapa Era Uma Vez 200ml": {"coluna": "Sucos", "aba_st": None, "un_cx": 27, "cod": "5682", "ipi": 0.0},
            "Bebida de Maçã Papapa Era Uma Vez 200ml": {"coluna": "Sucos", "aba_st": None, "un_cx": 27, "cod": "5683", "ipi": 0.0},
        },
        "ACHOCOLATADO": {
            "Bebida Láctea UHT Chocolate Papapa Era Uma Vez 200ml": {"coluna": "Achocolatado", "aba_st": None, "un_cx": 27, "cod": "5685", "ipi": 0.0},
        }
    },
    "PUERICULTURA": {
        "TALHERES": {
            "Kit De Talheres Infantil - Azul": {"coluna": "Puer. Talheres", "aba_st": None, "un_cx": 1, "cod": "5641", "ipi": 0.065},
            "Kit De Talheres Infantil - Verde": {"coluna": "Puer. Talheres", "aba_st": None, "un_cx": 1, "cod": "5658", "ipi": 0.065},
            "Kit De Talheres Infantil - Rosa": {"coluna": "Puer. Talheres", "aba_st": None, "un_cx": 1, "cod": "5665", "ipi": 0.065},
        },
        "BABADORES": {
            "Babador Infantil Com Bolso - Azul": {"coluna": "Puer. Babador", "aba_st": None, "un_cx": 1, "cod": "5733", "ipi": 0.065},
            "Babador Infantil Com Bolso - Verde": {"coluna": "Puer. Babador", "aba_st": None, "un_cx": 1, "cod": "5740", "ipi": 0.065},
            "Babador Infantil Com Bolso - Rosa": {"coluna": "Puer. Babador", "aba_st": None, "un_cx": 1, "cod": "5757", "ipi": 0.065},
        },
        "BOWLS": {
            "Bowl Infantil Com Ventosa - Azul": {"coluna": "Puer. Bolw", "aba_st": None, "un_cx": 1, "cod": "5702", "ipi": 0.065},
            "Bowl Infantil Com Ventosa - Verde": {"coluna": "Puer. Bolw", "aba_st": None, "un_cx": 1, "cod": "5719", "ipi": 0.065},
            "Bowl Infantil Com Ventosa - Rosa": {"coluna": "Puer. Bolw", "aba_st": None, "un_cx": 1, "cod": "5726", "ipi": 0.065},
        },
        "PRATINHOS": {
            "Pratinho Infantil Com Ventosa - Azul": {"coluna": "Puer. Pratinho", "aba_st": None, "un_cx": 1, "cod": "5675", "ipi": 0.065},
            "Pratinho Infantil Com Ventosa - Verde": {"coluna": "Puer. Pratinho", "aba_st": None, "un_cx": 1, "cod": "5689", "ipi": 0.065},
            "Pratinho Infantil Com Ventosa - Rosa": {"coluna": "Puer. Pratinho", "aba_st": None, "un_cx": 1, "cod": "5696", "ipi": 0.065},
        }
    }
}

if "aba_selecionada" not in locals() and "aba_selecionada" not in globals():
    aba_selecionada = "🛒 Simulador de Pedidos"

if aba_selecionada == "🏠 Home":
    st.write("Bem-vindo ao Playbook")

elif aba_selecionada == "🛒 Simulador de Pedidos":
    col_titulo, col_limpar = st.columns([4, 1])

    with col_titulo:
        st.header("🛒 Simulador de Pedidos")

    with col_limpar:
        st.write("")
        if st.button("Limpar", use_container_width=True, key="btn_limpar_simulador"):
            for chave in list(st.session_state.keys()):
                if chave.startswith("sim_qtd_"):
                    st.session_state[chave] = 0

            st.session_state["cnpj_input"] = ""
            st.session_state["sim_forma_pagamento"] = ""
            st.session_state["sim_regime"] = "NÃO"
            st.session_state["sim_vendedor"] = ""
            st.session_state["sim_tabela"] = "Selecione uma tabela"
            st.session_state["sim_estado"] = "Selecione o Estado"
            st.session_state["sim_desconto"] = 0.0
            st.session_state["sim_observacoes"] = ""
            st.rerun()

    total_pedido = 0.0
    df_precos = None
    df_tabelas = None
    dicionario_st = {}
    total_com_desconto = 0.0
    valor_desconto = 0.0
    perc_desconto = 0.0
    itens_selecionados_para_pdf = []

    def formatar_cnpj(cnpj):
        cnpj = "".join(filter(str.isdigit, cnpj))
        if len(cnpj) == 14:
            return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
        return cnpj

    st.subheader("Dados do Cliente e Pagamento")
    c_cnpj, c_pag, c_vendedor, c_regime = st.columns(4)

    with c_cnpj:
        cnpj_digitado = st.text_input("CNPJ do Cliente:", placeholder="Digite apenas números", key="cnpj_input")
        cnpj_cliente = formatar_cnpj(cnpj_digitado)

        if cnpj_digitado and len("".join(filter(str.isdigit, cnpj_digitado))) != 14:
            st.caption(":red[CNPJ incompleto]")
        elif cnpj_digitado:
            st.caption(f":green[Formatado: {cnpj_cliente}]")

    with c_pag:
        opcoes_pagamento = ["", "PIX", "Boleto 1x - 30 dias", "Boleto 2x - 30/45 dias", "Boleto 3x - 30/45/60 dias", "Boleto 1x - 45 dias", "Boleto 2x - 45/60 dias", "Boleto 3x - 40/50/60 dias"]
        forma_pagamento = st.selectbox("Forma de Pagamento:", opcoes_pagamento, index=0, key="sim_forma_pagamento")

    with c_vendedor:
        opcoes_vendedor = ["", "Ana", "Pedro", "João Paulo", "Rodrigo"]
        vendedor_sel = st.selectbox("Vendedor:", opcoes_vendedor, index=0, key="sim_vendedor")

    with c_regime:
        regime_simples = st.selectbox("Regime SIMPLES?", ["NÃO", "SIM"], index=0, key="sim_regime")

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        tabela_sel = st.selectbox("Selecione a Tabela:", list(mapa_tabelas.keys()), index=0, key="sim_tabela")

    with c2:
        lista_estados = ["Selecione o Estado", "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"]
        estado_sel = st.selectbox("Selecione o Estado (UF):", lista_estados, index=0, key="sim_estado")

    if tabela_sel != "Selecione uma tabela" and estado_sel != "Selecione o Estado":
        arquivo_tabela = mapa_tabelas.get(tabela_sel)
        caminho_tabela = localizar_arquivo_tabela(arquivo_tabela, tabela_sel)

        df_precos, dicionario_st, df_tabelas = carregar_dados_completos_por_caminho(caminho_tabela)

        fator_preco = 0.90 if tabela_sel == "ESPECIAL REDE (-10%)" else 1.0

        if df_precos is not None:
            st.subheader("Itens do Pedido")

            for cat_principal, subcategorias in categorias_produtos.items():
                st.markdown(f"### {cat_principal}")

                for sub_cat, produtos in subcategorias.items():
                    with st.expander(sub_cat, expanded=True):
                        for nome_exibicao, config in produtos.items():
                            col_prod, col_un, col_qtd, col_sub = st.columns([3, 1, 1, 2])
                            un_cx = config["un_cx"]

                            preco_unit, st_unitario, ipi_unitario_cx, valor_caixa_total = calcular_valores_produto(
                                df_precos,
                                df_tabelas,
                                dicionario_st,
                                estado_sel,
                                regime_simples,
                                nome_exibicao,
                                config,
                                fator_preco
                            )

                            with col_prod:
                                st.write(f"**{nome_exibicao}**")
                                st.caption(
                                    f"Cod: {config['cod']} | Unit: {moeda_br(preco_unit)} | "
                                    f"ST/Un: {moeda_br(st_unitario)} | IPI/Cx: {moeda_br(ipi_unitario_cx)}"
                                )

                            with col_un:
                                st.write(f"{un_cx} un/cx")
                                st.caption(f"{moeda_br(valor_caixa_total)}/cx")

                            with col_qtd:
                                qtd_cx = st.number_input("Cx", min_value=0, step=1, key=f"sim_qtd_{nome_exibicao}", label_visibility="collapsed")

                            with col_sub:
                                subtotal = valor_caixa_total * qtd_cx
                                total_pedido += subtotal
                                st.write(moeda_br(subtotal))

                            if qtd_cx > 0:
                                qtd_itens = qtd_cx * un_cx
                                preco_unit_total = valor_caixa_total / un_cx if un_cx else 0.0
                                itens_selecionados_para_pdf.append({
                                    "codigo": config["cod"],
                                    "nome": nome_exibicao,
                                    "qtd_cx": qtd_cx,
                                    "qtd_itens": qtd_itens,
                                    "preco_unit_total": preco_unit_total,
                                    "subtotal": subtotal
                                })

            st.divider()

            col_total_1, col_total_2 = st.columns([2, 1])

            with col_total_2:
                perc_desconto = st.number_input(
                    "Desconto (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=0.0,
                    step=0.5,
                    key="sim_desconto"
                )

                modelo_observacoes = (
                    "• CNPJ:\n"
                    "• Estado:\n"
                    "• Inscrição Estadual (IE):\n"
                    "• Telefone financeiro:\n"
                    "• Telefone compras:\n"
                    "• E-mail financeiro:\n"
                    "• E-mail compras:\n"
                    "• Dados bancários e chave PIX:\n"
                    "• Tem protesto no Cenprot:\n"
                    "• Data de abertura do CNPJ:"
                )

                observacoes_pedido = st.text_area(
                    "Observações",
                    placeholder="Inclua informações relevantes sobre o orçamento...",
                    height=375,
                    key="sim_observacoes"
                )

            valor_desconto = total_pedido * (perc_desconto / 100)
            total_com_desconto = total_pedido - valor_desconto

            with col_total_1:
                st.metric("Total Bruto (com ST/IPI)", moeda_br(total_pedido))

                if perc_desconto > 0:
                    st.metric("Total Líquido", moeda_br(total_com_desconto), delta=f"- {moeda_br(valor_desconto)}")
                else:
                    st.write(f"**Total Líquido: {moeda_br(total_pedido)}**")

                st.caption("Modelo para copiar nas observações")
                st.code(modelo_observacoes, language=None)

            if total_com_desconto >= 800:
                st.success("✅ Pedido acima do valor mínimo!")
            elif total_pedido > 0:
                st.warning(f"Faltam {moeda_br(800 - total_com_desconto)} para o mínimo.")

    else:
        st.info("💡 Por favor, selecione a **Tabela de Preços** e o **Estado** acima para visualizar os produtos.")

############################################################################
# GERADOR DE PDF
############################################################################
if aba_selecionada == "🛒 Simulador de Pedidos" and "total_pedido" in locals() and total_pedido > 0:
    try:
        def texto_pdf(txt):
            return str(txt).encode("latin-1", "ignore").decode("latin-1")

        def moeda_pdf(valor):
            return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        def desenhar_cabecalho_tabela(pdf):
            w_cod = 32
            w_prod = 68
            w_qtd_cx = 18
            w_qtd_itens = 22
            w_preco_unit = 25
            w_subtotal = 25
            altura_header = 10

            pdf.set_fill_color(240, 240, 240)
            pdf.set_font("Arial", "B", 8)
            pdf.cell(w_cod, altura_header, "Cod.", 1, 0, "C", True)
            pdf.cell(w_prod, altura_header, "Produto", 1, 0, "C", True)
            pdf.cell(w_qtd_cx, altura_header, "Qtd Cx", 1, 0, "C", True)
            pdf.cell(w_qtd_itens, altura_header, "Qtd Itens", 1, 0, "C", True)
            pdf.cell(w_preco_unit, altura_header, texto_pdf("Preço Unit"), 1, 0, "C", True)
            pdf.cell(w_subtotal, altura_header, "Subtotal", 1, 1, "C", True)
            pdf.set_font("Arial", size=7)

        def gerar_pdf(dados_pedido, total_bruto, desconto_p, desconto_v, total_liq, estado, cnpj, pagto, vendedor, observacoes):
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            logo_path = "Papapa-azul.png"
            if os.path.exists(logo_path):
                pdf.image(logo_path, x=80, y=12, w=50)
                pdf.ln(35)
            else:
                pdf.ln(10)

            pdf.set_font("Arial", "B", 16)
            pdf.cell(190, 10, txt=texto_pdf("Orçamento de Pedido - Papapá - Era Uma Vez"), ln=True, align="C")
            pdf.ln(5)

            pdf.set_font("Arial", size=10)
            data_atual = pd.to_datetime("today").strftime("%d/%m/%Y")

            pdf.cell(190, 7, txt=texto_pdf(f"Data: {data_atual}"), ln=True)
            pdf.cell(190, 7, txt=texto_pdf(f"Estado: {estado}"), ln=True)

            if cnpj and str(cnpj).strip():
                pdf.cell(190, 7, txt=texto_pdf(f"CNPJ Cliente: {cnpj}"), ln=True)

            if pagto and str(pagto).strip():
                pdf.cell(190, 7, txt=texto_pdf(f"Forma de Pagamento: {pagto}"), ln=True)

            if vendedor and str(vendedor).strip():
                pdf.cell(190, 7, txt=texto_pdf(f"Vendedor: {vendedor}"), ln=True)

            pdf.ln(5)

            w_cod = 32
            w_prod = 68
            w_qtd_cx = 18
            w_qtd_itens = 22
            w_preco_unit = 25
            w_subtotal = 25
            altura_linha = 5

            desenhar_cabecalho_tabela(pdf)

            for item in dados_pedido:
                nome_p = texto_pdf(item["nome"])
                codigo = texto_pdf(item["codigo"])

                linhas_produto = pdf.multi_cell(w_prod - 2, altura_linha, nome_p, split_only=True)
                num_linhas = max(1, len(linhas_produto))
                h_total = max(10, num_linhas * altura_linha + 4)

                if pdf.get_y() + h_total > 275:
                    pdf.add_page()
                    desenhar_cabecalho_tabela(pdf)

                x = pdf.get_x()
                y = pdf.get_y()

                pdf.rect(x, y, w_cod, h_total)
                pdf.rect(x + w_cod, y, w_prod, h_total)
                pdf.rect(x + w_cod + w_prod, y, w_qtd_cx, h_total)
                pdf.rect(x + w_cod + w_prod + w_qtd_cx, y, w_qtd_itens, h_total)
                pdf.rect(x + w_cod + w_prod + w_qtd_cx + w_qtd_itens, y, w_preco_unit, h_total)
                pdf.rect(x + w_cod + w_prod + w_qtd_cx + w_qtd_itens + w_preco_unit, y, w_subtotal, h_total)

                pdf.set_xy(x, y + 2)
                pdf.cell(w_cod, h_total - 4, codigo, 0, 0, "C")

                pdf.set_xy(x + w_cod + 1, y + 2)
                pdf.multi_cell(w_prod - 2, altura_linha, nome_p, 0, "L")

                pdf.set_xy(x + w_cod + w_prod, y + 2)
                pdf.cell(w_qtd_cx, h_total - 4, str(item["qtd_cx"]), 0, 0, "C")
                pdf.cell(w_qtd_itens, h_total - 4, str(item["qtd_itens"]), 0, 0, "C")
                pdf.cell(w_preco_unit, h_total - 4, moeda_pdf(item["preco_unit_total"]), 0, 0, "C")
                pdf.cell(w_subtotal, h_total - 4, moeda_pdf(item["subtotal"]), 0, 0, "C")

                pdf.set_xy(x, y + h_total)

            pdf.ln(5)
            pdf.set_font("Arial", "B", 10)
            pdf.cell(160, 8, "Total Bruto:", 0, 0, "R")
            pdf.cell(30, 8, moeda_pdf(total_bruto), 0, 1, "C")

            if desconto_p > 0:
                pdf.set_text_color(200, 0, 0)
                pdf.cell(160, 8, f"Desconto ({desconto_p}%):", 0, 0, "R")
                pdf.cell(30, 8, f"- {moeda_pdf(desconto_v)}", 0, 1, "C")
                pdf.set_text_color(0, 0, 0)

            pdf.set_font("Arial", "B", 12)
            pdf.cell(160, 10, texto_pdf("TOTAL LÍQUIDO:"), 0, 0, "R")
            pdf.cell(30, 10, moeda_pdf(total_liq), 0, 1, "C")

            if observacoes and str(observacoes).strip():
                obs_txt = texto_pdf(observacoes).strip()
                linhas_obs = pdf.multi_cell(186, 5, obs_txt, split_only=True)
                altura_obs = max(12, len(linhas_obs) * 5 + 4)

                if pdf.get_y() + altura_obs + 25 > 275:
                    pdf.add_page()

                pdf.ln(6)
                pdf.set_font("Arial", "B", 9)
                pdf.cell(190, 6, texto_pdf("Observações:"), 0, 1, "L")

                x_obs = pdf.get_x()
                y_obs = pdf.get_y()

                pdf.rect(x_obs, y_obs, 190, altura_obs)
                pdf.set_xy(x_obs + 2, y_obs + 2)

                pdf.set_font("Arial", size=8)
                pdf.multi_cell(186, 5, txt=obs_txt, border=0, align="L")

                pdf.set_xy(x_obs, y_obs + altura_obs)

            pdf.ln(10)
            pdf.set_font("Arial", "I", 8)
            aviso = "*Este documento é apenas uma simulação de valores (orçamento) e não garante a reserva de estoque ou a efetivação do pedido comercial. Este informativo não possui validade fiscal."
            pdf.multi_cell(190, 5, txt=texto_pdf(aviso), align="C")

            return pdf.output(dest="S").encode("latin-1")

        observacoes_pedido = st.session_state.get("sim_observacoes", "")
        vendedor_pdf = st.session_state.get("sim_vendedor", "")

        pdf_bytes = gerar_pdf(
            itens_selecionados_para_pdf,
            total_pedido,
            perc_desconto,
            valor_desconto,
            total_com_desconto,
            estado_sel,
            cnpj_cliente,
            forma_pagamento,
            vendedor_pdf,
            observacoes_pedido
        )

        id_botao = f"btn_pdf_{estado_sel}_{total_com_desconto}_{perc_desconto}_{vendedor_pdf}"

        st.download_button(
            label="📄 Baixar Orçamento em PDF",
            data=pdf_bytes,
            file_name=f"Orcamento_{estado_sel}.pdf",
            mime="application/pdf",
            use_container_width=True,
            key=id_botao
        )

    except Exception as e:
        st.error(f"Erro ao gerar PDF: {e}")
