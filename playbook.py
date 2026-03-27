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
    st.markdown("💡 **Dica:** Use os botões no canto superior direito de cada bloco para copiar o texto rapidamente.")
    
    tabs = st.tabs([
        "🤝 Abordagem Inicial", 
        "🚀 Explicação de Mix (Curva A)", 
        "📝 Cadastro & Fechamento", 
        "🚚 Pós-Venda & Financeiro"
    ])
    
    # --- ABA 0: ABORDAGEM ---
    with tabs[0]:
        st.subheader("📞 Primeiro Contato (Leads)")
        
        with st.expander("⭐ Opção 1: Abordagem Consultiva (Recomendada)", expanded=True):
            st.code("""Olá, tudo bem?
Aqui é [SEU NOME], da Papapá.
Vi que você se cadastrou na nossa página e quis entrar em contato para entender um pouco melhor o seu perfil e te indicar as melhores opções do nosso portfólio.
Você poderia me contar rapidamente que tipo de estabelecimento você tem?""", language=None)

        with st.expander("🏢 Opção 2: Foco em Perfil de Negócio"):
            st.code("""Oi, tudo bem?
Sou [SEU NOME], da Papapá.
Que legal ver seu interesse em trabalhar com nossos produtos!
Antes de te apresentar o portfólio completo, queria entender um pouco mais sobre o seu negócio, para te indicar as melhores opções e condições.
Você pode me contar rapidamente como funciona hoje?""", language=None)

        with st.expander("✅ Opção 3: Perguntas de Qualificação (Checklist)"):
            st.code("""Antes de te indicar os produtos, queria entender rapidinho:
• Que tipo de estabelecimento você tem?
• Em qual cidade/bairro?
• Seu público é mais família, fitness ou geral?""", language=None)

        with st.expander("📩 Opção 4: Abordagem mais direta"):
            st.code("""Olá, tudo bem? Aqui é o João, da Papapá.
Recebi seu cadastro e quis agradecer pelo interesse. A Papapá trabalha com uma linha de alimentação natural e pronta para bebês e crianças, sem conservantes e com ótima aceitação.
Posso te enviar o catálogo e as condições comerciais e, na sequência, entender se faz sentido para o seu negócio?""", language=None)

    # --- ABA 1: CURVA A ---
    with tabs[1]:
        st.subheader("🚀 Como explicar o Mix e Giro")
        st.info("Use estes scripts para converter clientes que estão em dúvida sobre o que comprar no primeiro pedido.")
        
        with st.expander("💎 Script: A Força da Curva A", expanded=True):
            st.code("""Pra te orientar melhor, vou te explicar como funciona o nosso mix e por onde indicamos começar. 
Hoje, a nossa Curva A (maior giro e recompra) é formada por:

• Papinhas de fruta – Nosso carro-chefe. Naturais, sem açúcar e não precisam de refrigeração.
• Biscoito Dentição – Snack funcional muito procurado por pais, com ótima saída por impulso.
• Biscotti – Nosso snack mais vendido, agrada bebês e até adultos.

Normalmente, quando o cliente começa pela Curva A, ele sente o giro rápido e depois amplia o mix com Palitinhos e Yoguzinho para aumentar o ticket médio.""", language=None)

        with st.expander("🛒 Script: Pergunta para entender primeiro pedido"):
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
            
        with col2:
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
        
        with st.expander("📦 Script: Confirmação e Fluxo Logístico", expanded=True):
            st.code("""Pedido efetuado com sucesso! Nosso fluxo funciona assim:
• Até 3 dias úteis para separação no CD.
• Mais 2 dias úteis para faturamento da NF.
• Em seguida, coleta da transportadora.
As NFs e boletos chegam direto no seu e-mail cadastrado!""", language=None)

        with st.expander("🚨 Script: Instrução de Recebimento (EVITA PREJUÍZO)"):
            st.warning("Envie este texto SEMPRE que o pedido for faturado.")
            st.code("""Uma orientação importante sobre o recebimento:
No momento da entrega, confira a mercadoria ANTES de assinar o canhoto.
Se houver caixa amassada, molhada ou produto quebrado:
1. Registre a RESSALVA na Nota Fiscal descrevendo o erro.
2. Não aceite os produtos avariados.
3. Me informe imediatamente.
Sem a ressalva na NF, a transportadora não aceita a reclamação e não conseguimos repor a mercadoria.""", language=None)

        with st.expander("💳 Script: Contato Financeiro"):
            st.code("""Para assuntos financeiros (2ª via de boleto, prorrogações ou comprovantes), fale direto com nosso time especializado:
📧 E-mail: contasareceber2@papapa.com.br""", language=None)

        with st.expander("🔄 Script: Regra de Troca (Validade)"):
            st.code("""Sobre trocas por validade:
A Papapá realiza a troca se o produto for entregue com menos de 60% da validade total.
Para isso, precisamos da emissão da NFD (Nota Fiscal de Devolução) constando:
• Número da NF de origem
• Motivo da devolução
• Lote do produto""", language=None)

################################################################################
# --- MÓDULO 5: POLÍTICAS COMERCIAIS ---
################################################################################
elif aba_selecionada == "📊 Políticas Comerciais":
    st.header("📊 Políticas Comerciais")
    
    # Destaques Rápidos
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pedido Mínimo", "R$ 800,00")
    c2.metric("Frete", "CIF (Grátis)")
    c3.metric("Prazo Saída", "5 dias úteis")
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
        - **Yoguzinho:** 16 unidades
        - **Palitinhos:** 16 unidades
        - **La Chef:** 6 unidades
        - **Sopinhas:** 6 unidades
        - **Papinhas de Fruta:** 12 unidades
        - **Papinhas de Carne:** 12 unidades
        - **Dentição:** 12 unidades
        - **Macarrão:** 12 unidades
        - **Cereal:** 12 unidades
        - **Biscotti:** 12 unidades
        """)

    # ESTE BLOCO ABAIXO FOI CORRIGIDO (Adicionados 4 espaços de indentação)
    with col_info2:
        st.subheader("💳 Modalidades de Pagamento")
        
        # CSS para deixar o texto dentro dos expanders idêntico ao print
        st.markdown("""
            <style>
            .pagamento-texto {
                font-size: 16px;
                line-height: 1.6;
                color: #31333F;
            }
            .highlight {
                background-color: #f0f2f6;
                padding: 2px 6px;
                border-radius: 4px;
                font-weight: bold;
            }
            </style>
        """, unsafe_allow_html=True)

        with st.expander("Prazos: Sul e Sudeste", expanded=True):
            st.markdown("""
            <div class="pagamento-texto">
            • <b>Até R$ 1.000:</b> <span class="highlight">30 dias</span><br>
            • <b>R$ 1.000 a R$ 2.000:</b> <span class="highlight">30/45 dias</span><br>
            • <b>Acima de R$ 2.000:</b> <span class="highlight">30/45/60 dias</span>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Prazos: Demais Regiões (NO/NE/CO/MG/ES)"):
            st.markdown("""
            <div class="pagamento-texto">
            • <b>Até R$ 1.000:</b> <span class="highlight">45 dias</span><br>
            • <b>R$ 1.000 a R$ 2.000:</b> <span class="highlight">45/60 dias</span><br>
            • <b>Acima de R$ 2.000:</b> <span class="highlight">40/50/60 dias</span>
            </div>
            """, unsafe_allow_html=True)
            
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
