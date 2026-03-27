import streamlit as st
import pandas as pd
import base64
from pathlib import Path

import streamlit as st
import base64

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
            Hub Inside Sales
        </h1>
    </div>
    """, unsafe_allow_html=True)

# Lista de opções exatamente como nos seus IFs
opcoes_menu = [
    "🏠 Home (Equipe)", 
    "💰 Simulador de Bonificação", 
    "📄 Biblioteca de Arquivos", 
    "✍️ Templates & Scripts", 
    "📊 Políticas Comerciais", 
    "🛠️ Resolução de Problemas",
    "🚫 Quebras de Excuses",
    "🔗 Links Úteis"
]

if 'aba_atual' not in st.session_state:
    st.session_state.aba_atual = "🏠 Home (Equipe)"

# Criamos as colunas e injetamos os botões
cols = st.columns(len(opcoes_menu))

for i, label in enumerate(opcoes_menu):
    with cols[i]:
        if st.button(label, key=f"btn_{label}", use_container_width=True):
            st.session_state.aba_atual = label

aba_selecionada = st.session_state.aba_atual
st.divider()
    
################################################################################
# --- MÓDULO 1: HOME (VISUALIZAÇÃO DA EQUIPE REFORMULADA) ---
################################################################################
if aba_selecionada == "🏠 Home (Equipe)":
    st.header("👥 Nossa Equipe")
    st.write("Conheça o time Inside Sales da Papapá.")

    # NOVA ESTRUTURA CSS PARA CENTRALIZAR E PADRONIZAR AS FOTOS
    st.markdown("""
        <style>
        .team-card {
            background-color: white; padding: 20px; border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.08); text-align: center;
            margin-bottom: 20px; border: 1px solid #eaeaea;
            height: 330px; /* Mantém todos os cards com o mesmo tamanho vertical */
            display: flex; flex-direction: column; align-items: center; justify-content: start;
        }

        /* O CÍRCULO DA FOTO */
        .photo-circle {
            width: 140px; height: 140px; border-radius: 50%;
            border: 4px solid #007bff; margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            background-size: cover; /* A mágica acontece aqui: centraliza e preenche */
            background-position: center top; /* Centraliza a foto de todos */
            background-repeat: no-repeat;
        }

        /* AJUSTE EXCLUSIVO PARA A FOTO DO JOÃO VITOR - POSICIONAMENTO MANUAL */
        /* Para corrigir a posição da cabeça no card do João Vitor, adicionei esta classe. */
        .photo-joao-vitor {
            background-position: center 20%; /* Ajuste manual para subir a cabeça dele */
        }
        
        /* AJUSTE EXCLUSIVO PARA A FOTO DA ANA - POSICIONAMENTO MANUAL */
        /* Para centralizar o rosto da Ana, adicionei esta classe. */
        .photo-ana {
            background-position: center 10%; /* Ajuste manual para o rosto dela */
        }

        /* AJUSTE EXCLUSIVO PARA A FOTO DO JOÃO PAULO - POSICIONAMENTO MANUAL */
        /* Para centralizar o rosto do João Paulo, adicionei esta classe. */
        .photo-joao-paulo {
            background-position: center 10%; /* Ajuste manual para o rosto dele */
        }

        /* AJUSTE EXCLUSIVO PARA A FOTO DO BERNARDO - POSICIONAMENTO MANUAL */
        /* Para centralizar o rosto do Bernardo, adicionei esta classe. */
        .photo-bernardo {
            background-position: center 10%; /* Ajuste manual para o rosto dele */
        }

        .team-name { font-weight: bold; font-size: 1.2em; color: #333; margin-bottom: 6px; }
        .team-role { color: #666; font-size: 1.0em; margin-bottom: 0px; font-weight: 500;}
        </style>
        """, unsafe_allow_html=True)

    # Lista da equipe com os nomes dos arquivos. Garanta que as extensões sejam .jpeg
    # Mantenha os arquivos antigos, mas use os arquivos novos de foco em rostos para obter o melhor resultado.
    equipe = [
        {"nome": "João Vitor Tadra", "cargo": "Coordenador", "foto": "João Vitor.jpeg", "classe_foto": "photo-joao-vitor"},
        {"nome": "Ana Christina Rodrigues", "cargo": "Analista - Key Accounts", "foto": "Ana.jpeg", "classe_foto": "photo-ana"},
        {"nome": "Pedro Henrique Born", "cargo": "Analista - Crescimento", "foto": "Pedro.jpeg", "classe_foto": "photo-pedro"},
        {"nome": "Joao Paulo Ferreira Alves", "cargo": "Analista - Desenvolvimento", "foto": "João Paulo.jpeg", "classe_foto": "photo-joao-paulo"},
        {"nome": "Thiago Martins Cabral", "cargo": "Estagiário - Operação", "foto": "Thiago.jpeg", "classe_foto": ""},
        {"nome": "Bernardo Oliveira Dallegrave", "cargo": "Estagiário - Operação", "foto": "Bernardo.jpeg", "classe_foto": "photo-bernardo"}
    ]
    
    # Criação de colunas para os cards (máximo 3 por linha)
    for i in range(0, len(equipe), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(equipe):
                membro = equipe[i + j]
                
                # Lógica para carregar a foto específica ou o logo padrão
                caminho_foto = membro['foto']
                classe_extra = membro['classe_foto']
                
                # Verifica se o arquivo existe e se tem conteúdo (size > 0)
                if Path(caminho_foto).exists() and Path(caminho_foto).stat().st_size > 0:
                    try:
                        foto_base64 = get_base64_of_bin_file(caminho_foto)
                        # Identifica a extensão para o cabeçalho base64
                        ext = caminho_foto.split('.')[-1].lower()
                        # Trata jpg como jpeg no cabeçalho
                        if ext == 'jpg': ext = 'jpeg'
                        # Define a imagem como plano de fundo (background-image)
                        estilo_foto = f"background-image: url('data:image/{ext};base64,{foto_base64}');"
                    except:
                        # Fallback se a conversão falhar
                        estilo_foto = f"background-image: url('{img_avatar_html}');"
                else:
                    # Se não achar a foto da pessoa (como Thiago e Bernardo), usa o logo Papapá
                    estilo_foto = f"background-image: url('{img_avatar_html}');"

                with cols[j]:
                    st.markdown(f"""
                        <div class="team-card">
                            <div class="photo-circle {classe_extra}" style="{estilo_foto}" title="{membro['nome']}"></div>
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
# --- MÓDULO 6: RESOLUÇÃO DE PROBLEMAS ---
################################################################################
elif aba_selecionada == "🛠️ Resolução de Problemas":
    st.header("🛠️ Resolução de Problemas")
    
    # Inicializa o contador de chave para o uploader
    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = 0

    col_conteudo, col_notas = st.columns([1.5, 1])

    with col_conteudo:
        st.info("🚧 **Em breve:** Fluxogramas de tratativa de avarias, faltas e devoluções logísticas.")
        st.image("https://img.freepik.com/vetores-gratis/projeto-do-conceito-do-ajuste-da-ferramenta_24877-50608.jpg", width=300)

    with col_notas:
        st.subheader("📝 Registro de Casos Críticos")
        
        if "historico_problemas" not in st.session_state:
            st.session_state.historico_problemas = []

        # --- FUNÇÃO CALLBACK PARA SALVAR ---
        def salvar_nota_callback():
            autor = st.session_state.get("nome_usuario_log")
            texto = st.session_state.get("input_area_problemas", "").strip()
            nf_pedido = st.session_state.get("input_nf_problema", "").strip() # Captura a NF
            
            chave_atual = f"input_foto_prob_{st.session_state.uploader_key}"
            arquivo_foto = st.session_state.get(chave_atual)
            
            if autor and texto:
                from datetime import datetime
                agora = datetime.now()
                meses_pt = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
                mes_atual = f"{meses_pt[agora.month - 1]}/2026"
                
                foto_bytes = None
                if arquivo_foto is not None:
                    foto_bytes = arquivo_foto.getvalue()
                
                nova_nota = {
                    "id_unico": agora.timestamp(),
                    "autor": autor,
                    "texto": texto,
                    "nf_pedido": nf_pedido, # Garante que a NF entre no dicionário
                    "foto": foto_bytes,
                    "data": agora.strftime("%d/%m/%Y %H:%M"),
                    "mes_referencia": mes_atual
                }
                
                st.session_state.historico_problemas.insert(0, nova_nota)
                
                # REGRAS DE LIMPEZA
                st.session_state["input_area_problemas"] = "" 
                st.session_state["input_nf_problema"] = ""    
                st.session_state.uploader_key += 1           
                
                st.toast("✅ Registro salvo com sucesso!")
            else:
                st.error("Preencha o nome e o texto antes de salvar.")

        # 1. Cadastro de Nova Nota
        with st.expander("➕ Registrar Ocorrência", expanded=True):
            lista_pessoas = ["João Tadra", "Ana", "Pedro", "João Paulo", "Bernardo", "Thiago"]
            
            st.selectbox(
                "Quem está registrando?", 
                lista_pessoas, 
                index=None, 
                placeholder="Selecione seu nome...",
                key="nome_usuario_log"
            )

            # Campo NF
            st.text_input(
                "Número da NF ou Pedido:",
                placeholder="Ex: NF 12345...",
                key="input_nf_problema"
            )

            st.text_area(
                "Descreva a ocorrência:", 
                key="input_area_problemas",
                height=100
            )

            st.file_uploader(
                "Anexar foto:", 
                type=["png", "jpg", "jpeg"],
                key=f"input_foto_prob_{st.session_state.uploader_key}"
            )

            st.button("Salvar Registro", use_container_width=True, on_click=salvar_nota_callback)

        st.divider()

        # 2. Filtro
        meses_filtro = ["Todos"] + [f"{m}/2026" for m in ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                                                        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]]
        filtro_mes = st.selectbox("Filtrar por mês", meses_filtro)

        # 3. Listagem (Ajustada para mostrar a NF)
        notas_exibidas = st.session_state.historico_problemas
        if filtro_mes != "Todos":
            notas_exibidas = [n for n in st.session_state.historico_problemas if n.get('mes_referencia') == filtro_mes]

        if not notas_exibidas:
            st.caption("Nenhum registro encontrado.")
        else:
            for idx, item in enumerate(notas_exibidas):
                with st.container():
                    c_txt, c_del = st.columns([0.85, 0.15])
                    with c_txt:
                        st.caption(f"📅 {item.get('data')} | 📂 {item.get('mes_referencia')}")
                        
                        # LOGICA DE EXIBIÇÃO DA NF AQUI:
                        nf_para_mostrar = item.get('nf_pedido', '').strip()
                        if nf_para_mostrar:
                            st.markdown(f"**🏷️ NF/Pedido:** `{nf_para_mostrar}`")
                            
                        st.write(f"**{item.get('autor')}:** {item.get('texto')}")
                        
                        if item.get("foto"):
                            st.image(item["foto"], width=250)
                    
                    with c_del:
                        if st.button("🗑️", key=f"del_{item.get('id_unico')}"):
                            st.session_state.historico_problemas.remove(item)
                            st.rerun()
                    st.markdown("---")
                    
################################################################################
# --- MÓDULO 7: QUEBRAS DE EXCUSES ---
################################################################################
elif aba_selecionada == "🚫 Quebras de Excuses":
    st.header("🚫 Quebras de Excuses")
    
    st.markdown("""
    <div style="background-color: #fff3cd; padding: 20px; border-radius: 10px; border-left: 5px solid #ffca28;">
        <h4 style="color: #856404; margin-top: 0;">⏳ Em construção...</h4>
        <p style="color: #856404;">Estamos mapeando as principais objeções (preço, giro, concorrência) para trazer os melhores argumentos para o time.</p>
    </div>
    """, unsafe_allow_html=True)

################################################################################
# --- MÓDULO 8: LINKS ÚTEIS ---
################################################################################
elif aba_selecionada == "🔗 Links Úteis":
    st.title("🔗 Central de Links Úteis")
    st.write("Acesse rapidamente as ferramentas e formulários da nossa operação.")
    
    # --- BLOCO ATUALIZADO: FERRAMENTAS DE TRABALHO (3 COLUNAS) ---
    with st.container():
        st.subheader("🛠️ Ferramentas de Trabalho (Daily)")
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
        st.subheader("📝 Cadastro e Operação")
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("📄 Forms Cadastro", "https://forms.office.com/pages/responsepage.aspx?id=KcXm9q-wZUOFUmPbM0a-aQ0xpHiomcxDhUissuWVgb9UMVU4UzNNWkc1REM3Vlk0SzVQMlZLSU5BWS4u&route=shorturl", use_container_width=True)
            st.caption("Novo cadastro e atualização de clientes")
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
    t1, t2, t3, t4 = st.columns(4) # Alterado para 4 colunas
    
    with t1:
        st.markdown("**Translovato**")
        st.link_button("Rastrear Lovato", "https://www.translovato.com.br/portal/rastreamento", use_container_width=True)
        st.code("User: BABY\nPass: Papapa@123")
        
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

    with st.container():
        st.subheader("🎨 Marketing e Divulgação")
        col_m1, col_m2 = st.columns([1, 2])
        with col_m1:
            st.link_button("📂 Drive para Lojistas", "https://papapacombr-my.sharepoint.com/:f:/g/personal/bi_papapa_com_br/EkwEgijW7pNCm95ElhfbiHoBK4kVtHiWieDpIOmwFZwRgA", use_container_width=True)
        with col_m2:
            st.warning("**Senha de acesso:** Papapa@2023")
            st.write("Compartilhe com o cliente para fotos, logos e materiais de PDV.")
