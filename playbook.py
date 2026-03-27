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
    st.write("Central de downloads para todos os materiais oficiais da Papapá.")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📁 Materiais de Venda")
        # Lista de arquivos para download
        arquivos_venda = {
            "📖 Catálogo Digital (PDF)": "catalogo-papapa-digital.pdf",
            "💰 Tabela de Preços (Excel)": "Tabela de preços Papapá 0226 v2.xlsx",
            "ℹ️ Ficha Técnica de Produtos": "Informações todos os produtos Papapá.pdf"
        }
        for label, path in arquivos_venda.items():
            with open(path, "rb") as f:
                st.download_button(label, f, file_name=path, use_container_width=True)

    with col2:
        st.subheader("📋 Guias e Processos")
        arquivos_processo = {
            "🎯 Estrutura de Metas e Operação": "Estrutura de Operação e Metas - Inside Sales.pdf",
            "📦 Guia de Recebimento (Avarias)": "GUIA DE RECEBIMENTO DE MERCADORIAS.pdf",
            "📝 Templates de Mensagens (PDF)": "Templates IS 2026.docx (2).pdf"
        }
        for label, path in arquivos_processo.items():
            with open(path, "rb") as f:
                st.download_button(label, f, file_name=path, use_container_width=True)

# --- MÓDULO 4: LOGÍSTICA & SAC ---
elif aba_selecionada == "🚚 Logística & SAC":
    st.title("🚚 Logística & SAC")
    st.subheader("Principais Regras de Recebimento")
    
    st.warning("**Atenção:** Entregas sem ressalva na Nota Fiscal não serão reconhecidas pela logística.")
    
    with st.expander("🔍 O que conferir no ato da entrega?"):
        st.write("""
        - Caixas amassadas ou rasgadas.
        - Embalagens violadas ou produtos quebrados.
        - Divergência entre físico e Nota Fiscal.
        """)
        
    with st.expander("🔄 Procedimento para Avarias"):
        st.write("""
        1. **Registrar Ressalva:** Descrever o problema no verso da NF.
        2. **Recusa Parcial:** Se apenas parte estiver ruim, recuse apenas os itens avariados.
        3. **NFD:** O cliente deve emitir a Nota Fiscal de Devolução para os itens recusados.
        """)

    st.subheader("⏱️ Prazos e Processos")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.info("**Faturamento:** Até 2 dias úteis após a separação.")
    with col_p2:
        st.info("**Separação:** Até 3 dias úteis após confirmação.")

import streamlit as st

# --- 1. CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(
    page_title="Papapá | Sales Hub",
    page_icon="💙",
    layout="wide"
)

# --- 2. CSS CUSTOMIZADO (Identidade Papapá) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fb; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #eee; }
    h1, h2, h3 { color: #004a99 !important; font-family: 'Segoe UI', sans-serif; }
    
    /* Estilo das Abas */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 15px 15px 0 0;
        padding: 10px 20px;
        border: 1px solid #eee;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #004a99;
        color: white !important;
    }
    
    /* Blocos de Código/Templates */
    .stCode { border: 1px solid #d1d9e0; border-radius: 10px; background-color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (APENAS 2 MENUS) ---
st.sidebar.image("https://papapa.com.br/wp-content/uploads/2021/06/logo-papapa.png", width=120)
st.sidebar.title("Navegação")

menu = st.sidebar.radio(
    "Ir para:",
    ["✍️ Templates de Mensagens", "📋 Políticas e Prazos"]
)

# --- 4. MÓDULO: TEMPLATES DE MENSAGENS ---
if menu == "✍️ Templates de Mensagens":
    st.title("✍️ Hub de Templates & Scripts")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🤝 Abordagem", "🚀 Curva A", "📝 Cadastro/PIX", "🚚 Logística", "🛠️ Pós-Venda"
    ])

    with tab1:
        st.subheader("Modelos de Abordagem e Sondagem")
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("Aproximação Clássica (Lojista)", expanded=True):
                st.code("Olá, tudo bem?\nAqui é o [Seu Nome], da Papapá.\nVi que você se cadastrou na nossa página e quis entrar em contato para entender um pouco melhor o seu perfil e te indicar as melhores opções do nosso portfólio.\nVocê poderia me contar rapidamente que tipo de estabelecimento você tem?", language=None)
            
            with st.expander("Abordagem Assertiva (Foco Negócio)"):
                st.code("Oi, tudo bem?\nSou o [Seu Nome], da Papapá.\nVi que você se cadastrou para receber mais informações. Antes de te enviar o material, queria só entender melhor o seu perfil pra te mandar algo mais assertivo.\nVocê trabalha com qual tipo de negócio?", language=None)

        with col2:
            with st.expander("Interesse em Catálogo", expanded=True):
                st.code("Oi, tudo bem?\nSou o [Seu Nome], da Papapá.\nQue legal ver seu interesse em trabalhar com nossos produtos!\nAntes de te apresentar o portfólio completo, queria entender um pouco mais sobre o seu negócio, para te indicar as melhores opções e condições.\nVocê pode me contar rapidamente como funciona hoje?", language=None)

    with tab2:
        st.subheader("🚀 Estratégia de Mix (Curva A)")
        st.info("Dica: Use este script para garantir o giro rápido no cliente novo.")
        st.code("""Vou te explicar rapidamente como funciona o nosso mix e por onde normalmente indicamos começar.
Hoje, a nossa Curva A (produtos de maior giro e recompra) é formada por:
• Papinhas de fruta – Nosso carro-chefe. Sem adição de açúcar e não precisam de refrigeração.
• Biscoitinho para fase da dentição – Snack funcional com alta procura.
• Biscotti – Nosso snack mais vendido, naturalmente adocicado pelas frutas.

Em um segundo momento, entram como complemento:
• Palitinhos de vegetais – Assados e fonte de proteínas.
• Yoguzinho – Shelf Life de 15 meses (fora de geladeira).""", language=None)

    with tab3:
        st.subheader("📝 Cadastro e Dados Financeiros")
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Documentos para Cadastro:**")
            st.code("● CNPJ:\n● Inscrição Estadual (IE):\n● Telefone Financeiro:\n● Telefone Compras:\n● E-mail Financeiro:\n● E-mail Compras:\n● Dados Bancários (pix):", language=None)
        with c2:
            st.write("**Dados para Pagamento (PIX/Itaú):**")
            st.code("Pix: CNPJ 34.282.307/0001-44\nBABY ROO COMERCIO DE ALIMENTOS S/A\n\nTransferência Itaú:\nAg 8931 | CC 05510-0", language=None)

    with tab4:
        st.subheader("🚚 Logística e Fluxo de Pedido")
        st.code("""🔹 Pedido Mínimo: R$ 800,00.\n🔹 Venda: Caixas Fechadas.\n🔹 Frete: CIF (Grátis) para todo o Brasil.\n\nFluxo de Prazo:\n• Até 3 dias úteis para separação.\n• + 2 dias úteis para faturamento.\n• Após isso, segue para coleta da transportadora.""", language=None)

    with tab5:
        st.subheader("🛠️ Gestão de Ocorrências (Avarias)")
        st.warning("Sem a ressalva na NF, a logística não aceita a reclamação!")
        st.code("""No momento da entrega, confira a mercadoria antes de assinar a NF.\nIdentificou avaria (embalagem violada, caixa amassada)?\n1. Registre a ressalva na Nota Fiscal.\n2. Não aceite os produtos avariados.\n3. Informe a Papapá imediatamente.""", language=None)

# --- 5. MÓDULO: POLÍTICAS E PRAZOS ---
if menu == "📋 Políticas e Prazos":
    st.title("📊 Políticas Comerciais Papapá")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("📅 Tabela de Validade (Shelf Life)")
        validade_data = {
            "Papinhas de Fruta": "16 meses", "Papinhas de Carne": "12 meses",
            "Yoguzinho": "15 meses", "Dentição": "15 meses",
            "Biscotti": "10 meses", "La Chef": "16 meses",
            "Macarrão": "14 meses", "Cereal": "12 meses",
            "Palitinhos": "9 meses", "Sopinhas": "12 meses"
        }
        st.table(validade_data)

    with col_b:
        st.subheader("💳 Prazos de Boleto")
        st.markdown("**Sul e Sudeste:**")
        st.code("Até 1k: 30d | 1k-2k: 30/45d | +2k: 30/45/60d", language=None)
        st.markdown("**Demais Regiões (NO/NE/CO/MG/ES):**")
        st.code("Até 1k: 45d | 1k-2k: 45/60d | +2k: 40/50/60d", language=None)
        st.divider()
        st.write("**Financeiro:** contasareceber2@papapa.com.br")
    
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
