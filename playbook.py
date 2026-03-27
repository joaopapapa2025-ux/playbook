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
            
        if perc_bonus == 0.0:
            st.error("A meta ainda não atingiu o piso de 90% para bonificação. Foco total em Reativação!")
        else:
            st.success(f"Bônus de {perc_bonus*100:.0f}% garantido sobre o salário base.")

# --- MÓDULO 3: BIBLIOTECA DE ARQUIVOS ---
elif aba_selecionada == "📄 Biblioteca de Arquivos":
    st.title("📄 Biblioteca de Arquivos")
    st.write("Baixe aqui os materiais atualizados para suporte às vendas.")

    # Criando colunas para organizar os arquivos por categoria
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📁 Materiais de Venda")
        
        # Arquivo: Catálogo Digital
        with open("catalogo-papapa-digital.pdf", "rb") as f:
            st.download_button(
                label="📖 Baixar Catálogo Digital (PDF)",
                data=f,
                file_name="catalogo-papapa-digital.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        # Arquivo: Tabela de Preços
        with open("Tabela de preços Papapá 0226 v2.xlsx", "rb") as f:
            st.download_button(
                label="💰 Baixar Tabela de Preços (Excel)",
                data=f,
                file_name="Tabela_de_Precos_Papapa_0226.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    with col2:
        st.subheader("📋 Guias e Informações")
        
        # Arquivo: Informações de Produtos
        with open("Informações todos os produtos Papapá.pdf", "rb") as f:
            st.download_button(
                label="ℹ️ Ficha Técnica de Produtos",
                data=f,
                file_name="Informacoes_Produtos_Papapa.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        # Arquivo: Estrutura Inside Sales
        with open("Estrutura de Operação e Metas - Inside Sales.pdf", "rb") as f:
            st.download_button(
                label="🎯 Estrutura de Metas e Operação",
                data=f,
                file_name="Estrutura_Metas_Inside_Sales.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# --- MANTENDO OS OUTROS PLACEHOLDERS ---
elif aba_selecionada == "🚚 Logística & SAC":
    st.title("🚚 Logística & SAC")
    with open("GUIA DE RECEBIMENTO DE MERCADORIAS.pdf", "rb") as f:
        st.download_button(
            label="📦 Baixar Guia de Recebimento (Avarias)",
            data=f,
            file_name="Guia_Recebimento_Mercadorias.pdf",
            mime="application/pdf"
        )
    st.info("As regras detalhadas de logística serão listadas aqui.")

elif aba_selecionada == "✍️ Templates & Scripts":
    st.title("✍️ Templates & Scripts")
    with open("Templates IS 2026.docx (2).pdf", "rb") as f:
        st.download_button(
            label="📝 Baixar Templates de Mensagens",
            data=f,
            file_name="Templates_Scripts_2026.pdf",
            mime="application/pdf"
        )
    st.info("Os scripts de WhatsApp/Email serão formatados para cópia rápida em breve.")

# --- MÓDULO 4, 5: PLACEHOLDERS (Para desenvolvimento futuro) ---

elif aba_selecionada == "🚚 Logística & SAC":
    st.title("🚚 Logística & SAC (Em Breve)")
    st.info("Esta aba será preenchida com as regras de recebimento e avarias.")

elif aba_selecionada == "✍️ Templates & Scripts":
    st.title("✍️ Templates & Scripts (Em Breve)")
    st.info("Esta aba será preenchida com os scripts de WhatsApp/Email.")

# --- MÓDULO 6: Links Úteis ---

elif aba_selecionada == "🔗 Links Úteis":
    st.title("🔗 Central de Links Úteis")
    st.write("Acesse rapidamente as ferramentas e formulários da nossa operação.")
    
    # --- SEÇÃO 1: CADASTRO E OPERAÇÃO ---
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

# --- SEÇÃO 2: DASHBOARDS E INDICADORES ---
with st.container():
    st.subheader("📊 Dashboards de Gestão")
    col_dash = st.columns(1)[0] # Coluna única para o dash principal
    
    with col_dash:
        st.link_button("📈 Dashboard Clientes", "https://dashboard-clientes-swsbdiavx4hfqvjbtcvafs.streamlit.app/", use_container_width=True)
        st.info("**Senha:** amamosnossosclientes")

    st.markdown("---")

    # --- SEÇÃO 3: LOGÍSTICA ---
    st.subheader("🚚 Logística e Rastreamento")
    
    # Sub-bloco para Solicitações
    c1, c2 = st.columns(2)
    with c1:
        st.link_button("🚩 Solicitações Logísticas", "https://forms.office.com/Pages/ResponsePage.aspx?id=KcXm9q-wZUOFUmPbM0a-aQpGwsStRQZMoYBHJmx0xW1UMDhXRkQwSEQxU0cwUklNNVVGWTZFRUhVNS4u", use_container_width=True)
    with c2:
        st.link_button("📂 Respostas Solicitações", "https://papapacombr-my.sharepoint.com/:x:/g/personal/operacoes_papapa_com_br/IQDfqtRILiD4R5lmLjQujLN3AS4On6breUbk-qRT2a0sUYk?rtime=_eVdf_F13kg", use_container_width=True)
    
    st.link_button("📍 Follow-up de Entregas (Sharepoint)", "https://papapacombr.sharepoint.com/:x:/r/sites/Papapa-Fileserver/_layouts/15/Doc.aspx?sourcedoc=%7B5cf28a24-1caa-4578-8641-a96b089efffa%7D&action=edit", use_container_width=True)

    # Cards para Transportadoras
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

    # --- SEÇÃO 4: MARKETING ---
    with st.container():
        st.subheader("🎨 Marketing e Divulgação")
        col_m1, col_m2 = st.columns([1, 2])
        
        with col_m1:
            st.link_button("📂 Drive para Lojistas", "https://papapacombr-my.sharepoint.com/:f:/g/personal/bi_papapa_com_br/EkwEgijW7pNCm95ElhfbiHoBK4kVtHiWieDpIOmwFZwRgA", use_container_width=True)
        
        with col_m2:
            st.warning("**Senha de acesso:** Papapa@2023")
            st.write("Compartilhe este link com o cliente para fotos, logos e materiais de PDV.")

