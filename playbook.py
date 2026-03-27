import streamlit as st
import pandas as pd
import base64
from pathlib import Path

################################################################################
# --- 1. CONFIGURAÇÕES DE ESTILO E PÁGINA ---
################################################################################
st.set_page_config(
    page_title="Papapá | Sales Hub 2026", 
    layout="wide", 
    page_icon="💙",
    initial_sidebar_state="collapsed"
)

# Função para carregar imagem e converter para base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Configuração da imagem do avatar
img_filename = "Papapa-azul..png"
if Path(img_filename).exists():
    img_base64 = get_base64_of_bin_file(img_filename)
    img_avatar_html = f"data:image/png;base64,{img_base64}"
else:
    img_avatar_html = "https://www.w3schools.com/howto/img_avatar.png" 

# CSS Customizado (Cards, Cores e Esconder Sidebar)
st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{ display: none; }} /* Remove menu lateral */
    div.row-widget.stRadio > div {{ flex-direction: row; gap: 20px; }} /* Radio Horizontal */
    
    h1 {{ color: #004a99; font-family: 'Segoe UI', sans-serif; }}
    
    .team-card {{
        background-color: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center;
        margin-bottom: 20px; border: 1px solid #eaeaea;
    }}
    .avatar-round {{
        width: 110px; height: 110px; border-radius: 50%;
        object-fit: cover; border: 3px solid #007bff; margin-bottom: 15px;
    }}
    .team-name {{ font-weight: bold; font-size: 1.1em; color: #333; margin-bottom: 5px; }}
    .team-role {{ color: #666; font-size: 0.9em; margin-bottom: 15px; }}
    .stCode {{ background-color: #fcfcfc; border-radius: 10px; border: 1px solid #e0e0e0; }}
    </style>
    """, unsafe_allow_html=True)

################################################################################
# --- 2. NAVEGAÇÃO SUPERIOR ---
################################################################################
st.title("Hub Inside Sales | Papapá")

aba_selecionada = st.radio(
    "Navegação:",
    ["🏠 Home (Equipe)", "💰 Simulador de Bonificação", "📄 Biblioteca de Arquivos", "✍️ Templates & Scripts", "📊 Políticas Comerciais", "🔗 Links Úteis"],
    horizontal=True
)

st.divider()

################################################################################
# --- MÓDULO 1: HOME (VISUALIZAÇÃO DA EQUIPE) ---
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
                membro = equipe[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="team-card">
                            <img src="{img_avatar_html}" class="avatar-round">
                            <div class="team-name">{membro['nome']}</div>
                            <div class="team-role">{membro['cargo']}</div>
                        </div>
                    """, unsafe_allow_html=True)

################################################################################
# --- MÓDULO 2: SIMULADOR DE BONIFICAÇÃO ---
################################################################################
elif aba_selecionada == "💰 Simulador de Bonificação":
    st.header("💰 Simulador de Comissionamento Individual")
    
    col_input, col_result = st.columns([1, 1.5])
    with col_input:
        salario_base = st.number_input("Seu Salário Fixo Base (R$)", min_value=0.0, value=3000.0)
        meta_mes = st.number_input("Valor da Meta do Mês (R$)", min_value=0.0, value=150000.0)
        resultado_atual = st.number_input("Seu Resultado Atual Batido (R$)", min_value=0.0, value=135000.0)
        
    with col_result:
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

################################################################################
# --- MÓDULO 3: BIBLIOTECA DE ARQUIVOS ---
################################################################################
elif aba_selecionada == "📄 Biblioteca de Arquivos":
    st.header("📄 Biblioteca de Arquivos")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📁 Materiais de Venda")
        arquivos_venda = {
            "📖 Catálogo Digital (PDF)": "catalogo-papapa-digital.pdf",
            "💰 Tabela de Preços (Excel)": "Tabela de preços Papapá 0226 v2.xlsx",
            "ℹ️ Ficha Técnica de Produtos": "Informações todos os produtos Papapá.pdf"
        }
        for label, path in arquivos_venda.items():
            try:
                with open(path, "rb") as f:
                    st.download_button(label, f, file_name=path, use_container_width=True)
            except FileNotFoundError: st.error(f"Arquivo não encontrado: {path}")

    with col2:
        st.subheader("📋 Guias e Processos")
        arquivos_proc = {
            "🎯 Estrutura de Operação e Metas": "Estrutura de Operação e Metas - Inside Sales.pdf",
            "📦 Guia de Recebimento de Mercadorias": "GUIA DE RECEBIMENTO DE MERCADORIAS.pdf",
            "📝 Templates (PDF)": "Templates IS 2026.docx (2).pdf"
        }
        for label, path in arquivos_proc.items():
            try:
                with open(path, "rb") as f:
                    st.download_button(label, f, file_name=path, use_container_width=True)
            except FileNotFoundError: st.error(f"Arquivo não encontrado: {path}")

################################################################################
# --- MÓDULO 4: TEMPLATES & SCRIPTS ---
################################################################################
elif aba_selecionada == "✍️ Templates & Scripts":
    st.header("✍️ Templates & Scripts")
    st.markdown("Use os botões no canto superior direito de cada bloco para copiar o texto.")
    
    tabs = st.tabs(["🤝 Abordagem Inicial", "🚀 Sugestão de Mix (Curva A)", "📝 Cadastro & Fechamento", "🚚 Pós-Venda & Financeiro"])
    
    with tabs[0]:
        st.subheader("Primeiro Contato (Lead Novo)")
        
        with st.expander("Opção 1: Abordagem Consultiva (Recomendada)", expanded=True):
            st.code("""Olá, tudo bem?
Aqui é o João, da Papapá.
Vi que você se cadastrou na nossa página e quis entrar em contato para entender um pouco melhor o seu perfil e te indicar as melhores opções do nosso portfólio.
Você poderia me contar rapidamente que tipo de estabelecimento você tem?""", language=None)

        with st.expander("Opção 2: Foco em Perfil de Negócio"):
            st.code("""Oi, tudo bem?
Sou o João, da Papapá.
Que legal ver seu interesse em trabalhar com nossos produtos!
Antes de te apresentar o portfólio completo, queria entender um pouco mais sobre o seu negócio, para te indicar as melhores opções e condições.
Você pode me contar rapidamente como funciona hoje?""", language=None)

        with st.expander("Opção 3: Perguntas de Qualificação (Checklist)"):
            st.code("""Antes de te indicar os produtos, queria entender rapidinho:
• Que tipo de estabelecimento você tem?
• Em qual cidade/bairro?
• Seu público é mais família, fitness ou geral?""", language=None)

    with tabs[1]:
        st.subheader("Explicação de Mix e Curva A")
        st.info("💡 Dica: Use este texto para converter clientes que não sabem por onde começar.")
        
        with st.expander("Script: Por que começar pela Curva A?", expanded=True):
            st.code("""Hoje a nossa Curva A, ou seja, os produtos que mais giram e que recomendamos para iniciar, são:

• Papinhas de fruta (carro-chefe) – Naturais, sem adição de açúcar e excelente aceitação.
• Biscoitinho Dentição – Snack funcional com compra recorrente e saída por impulso.
• Biscotti – Nosso snack mais vendido, agrada bebês e até adultos.

Esses três concentram a maior parte do volume. Em um segundo momento, entram os Palitinhos de Vegetais e o Yoguzinho para complementar o ticket.""", language=None)

        with st.expander("Script: Sugestão de Pedido Inicial"):
            st.code("""Pelo seu perfil, o que mais faz sentido hoje é começar com a Curva A, porque são os produtos com maior giro e recompra.
Hoje você imagina algo mais como teste ou já pensa em um pedido inicial pra abastecer gôndola?""", language=None)

    with tabs[2]:
        st.subheader("Fechamento e Condições")
        
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("Dados para Cadastro", expanded=True):
                st.code("""Para darmos sequência e liberar seu cadastro aqui na Papapá, preciso de:
• CNPJ:
• Inscrição Estadual (IE):
• Telefone Financeiro/Compras:
• E-mail Financeiro/Compras:
• Dados Bancários (pix):

*Obs.: É importante incluir a Descrição das Atividades (CNAE) de produtos alimentícios.""", language=None)
        
        with col2:
            with st.expander("Condições Comerciais (Resumo)"):
                st.code("""Vou te passar nossas condições pra você se organizar:
• Pedido mínimo: R$ 800,00.
• Pagamento: Pix ou Boleto.
• Entrega: Frete CIF (por nossa conta) para todo o Brasil.
• Venda: Por caixas fechadas (12 un. na maioria das linhas).""", language=None)

    with tabs[3]:
        st.subheader("Acompanhamento e Suporte")
        
        with st.expander("Confirmação de Pedido & Fluxo Logístico"):
            st.code("""Pedido efetuado com sucesso! Nosso fluxo funciona assim:
• Até 3 dias úteis para separação no CD.
• Mais 2 dias úteis para faturamento da NF.
• Em seguida, coleta da transportadora.
As NFs e boletos chegam direto no seu e-mail cadastrado!""", language=None)

        with st.expander("🚨 IMPORTANTE: Instrução de Recebimento"):
            st.warning("Envie isso para evitar problemas com avarias sem ressalva.")
            st.code("""Orientações para o recebimento:
É fundamental conferir a mercadoria antes de assinar a Nota Fiscal. 
Caso identifique caixas amassadas ou produtos quebrados:
1. Registre a ressalva na Nota Fiscal descrevendo o problema.
2. Não aceite os produtos avariados.
3. Me informe imediatamente!
Sem a ressalva na NF, a transportadora não aceita a reclamação.""", language=None)


################################################################################
# --- MÓDULO 5: POLÍTICAS COMERCIAIS ---
################################################################################
elif aba_selecionada == "📊 Políticas & Prazos":
    st.header("📊 Políticas Comerciais")
    
    # Destaques Rápidos
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pedido Mínimo", "R$ 800,00")
    c2.metric("Frete", "CIF (Grátis)")
    c3.metric("Prazo Saída", "5 Dias Úteis")
    c4.metric("Troca", "> 60% Shelf Life")

    st.divider()

    col_info1, col_info2 = st.columns(2)

    with col_info1:
        st.subheader("📅 Shelf Life (Validades)")
        validades = {
            "Linha": ["Papinhas de Fruta", "La Chef", "Yoguzinho", "Dentição", "Macarrão", "Sopinhas", "Carne", "Cereal", "Biscotti", "Palitinhos"],
            "Meses": [16, 16, 15, 15, 14, 12, 12, 12, 10, 9]
        }
        st.table(pd.DataFrame(validades))
        st.caption("❄️ Nenhuma linha necessita de refrigeração.")

        st.subheader("📦 Unidades por Caixa")
        st.markdown("""
        - **Palitinho e Yoguzinho:** 16 unidades
        - **La Chef e Sopinhas:** 6 unidades
        - **Demais Linhas:** 12 unidades
        """)

    with col_info2:
        st.subheader("💳 Modalidades de Pagamento")
        
        with st.expander("Prazos: Sul e Sudeste", expanded=True):
            st.write("- **Até R$ 1.000:** 30 dias")
            st.write("- **R$ 1.000 a R$ 2.000:** 30/45 dias")
            st.write("- **Acima de R$ 2.000:** 30/45/60 dias")

        with st.expander("Prazos: Demais Regiões (NO/NE/CO/MG/ES)"):
            st.write("- **Até R$ 1.000:** 45 dias")
            st.write("- **R$ 1.000 a R$ 2.000:** 45/60 dias")
            st.write("- **Acima de R$ 2.000:** 40/50/60 dias")
        
        st.success("**Pagamento:** Pix ou Boleto (enviado por e-mail)")

    st.divider()
    
    st.subheader("🔄 Política de Trocas e Devoluções")
    st.info("""A troca por validade reduzida só é aplicada se o produto chegar com **menos de 60% da validade total**. 
    É obrigatório o envio da NFD (Nota Fiscal de Devolução) com o número da NF de origem e lote.""")

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
