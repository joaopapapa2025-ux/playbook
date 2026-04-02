import streamlit as st
import pandas as pd
import os
from datetime import datetime
import base64
from pathlib import Path
from google.cloud import firestore
from google.oauth2 import service_account

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
    "📈 Impactos no resultado",
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

    # ESTRUTURA CSS CORRIGIDA E COMPACTA
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
            height: 350px; /* Altura reduzida para eliminar o espaço em branco */
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; /* Centraliza o conteúdo para evitar vácuo */
            transition: transform 0.3s;
        }
        
        .team-card:hover { transform: translateY(-5px); }

        .photo-circle {
            width: 125px; 
            height: 125px; 
            border-radius: 50%;
            border: 4px solid #007bff; 
            margin-bottom: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            background-size: cover;
            background-position: center top;
            background-repeat: no-repeat;
        }

        /* Ajustes Manuais de Enquadramento */
        .photo-joao-vitor { background-position: center 20%; }
        .photo-ana { background-position: center 10%; }
        .photo-joao-paulo { background-position: center 10%; }
        .photo-bernardo { background-position: center 10%; }

        .team-name { font-weight: bold; font-size: 1.1em; color: #333; margin-bottom: 2px; }
        .team-role { color: #666; font-size: 0.9em; margin-bottom: 10px; font-weight: 500; font-style: italic; }
        
        .contact-container {
            width: 100%;
            padding-top: 8px;
            border-top: 1px solid #eee;
        }

        .contact-link {
            text-decoration: none !important;
            color: #007bff !important;
            font-size: 0.82em;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }
        
        .whatsapp-icon {
            width: 16px;
            height: 16px;
            vertical-align: middle;
        }
        </style>
        """, unsafe_allow_html=True)

    # Lista da equipe com dados oficiais
    equipe = [
        {"nome": "João Vitor Tadra", "cargo": "Coordenador", "foto": "João Vitor.jpeg", "classe_foto": "photo-joao-vitor", "telefone": "(41) 98495-9492", "email": "comercial1@papapa.com.br"},
        {"nome": "Ana Christina Rodrigues", "cargo": "Analista - Key Accounts", "foto": "Ana.jpeg", "classe_foto": "photo-ana", "telefone": "(41) 3797-6554", "email": "comercial3@papapa.com.br"},
        {"nome": "Pedro Henrique Born", "cargo": "Analista - Crescimento", "foto": "Pedro.jpeg", "classe_foto": "photo-pedro", "telefone": "(41) 3797-6885", "email": "comercial5@papapa.com.br"},
        {"nome": "Joao Paulo Ferreira Alves", "cargo": "Analista - Desenvolvimento", "foto": "João Paulo.jpeg", "classe_foto": "photo-joao-paulo", "telefone": "(41) 99247-4213", "email": "comercial2@papapa.com.br"},
        {"nome": "Thiago Martins Cabral", "cargo": "Estagiário - Operação", "foto": "Thiago.jpeg", "classe_foto": "", "telefone": "(41) 98502-7025", "email": "comercial4@papapa.com.br"},
        {"nome": "Bernardo Oliveira Dallegrave", "cargo": "Estagiário - Operação", "foto": "Bernardo.jpeg", "classe_foto": "photo-bernardo", "telefone": "(41) 98470-3249", "email": "comercial6@papapa.com.br"}
    ]
    
    wa_icon_url = "https://cdn-icons-png.flaticon.com/512/733/733585.png"

    for i in range(0, len(equipe), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(equipe):
                membro = equipe[i + j]
                
                # Limpeza do número para o link
                numero_limpo = "".join(filter(str.isdigit, membro['telefone']))
                link_whatsapp = f"https://wa.me/55{numero_limpo}"
                
                caminho_foto = membro['foto']
                # Tenta carregar a imagem ou usa o avatar padrão
                if Path(caminho_foto).exists() and Path(caminho_foto).stat().st_size > 0:
                    try:
                        foto_base64 = get_base64_of_bin_file(caminho_foto)
                        ext = caminho_foto.split('.')[-1].lower()
                        if ext == 'jpg': ext = 'jpeg'
                        estilo_foto = f"background-image: url('data:image/{ext};base64,{foto_base64}');"
                    except:
                        estilo_foto = f"background-image: url('{img_avatar_html}');"
                else:
                    estilo_foto = f"background-image: url('{img_avatar_html}');"

                with cols[j]:
                    st.markdown(f"""
                        <div class="team-card">
                            <div class="photo-circle {membro['classe_foto']}" style="{estilo_foto}"></div>
                            <div class="team-name">{membro['nome']}</div>
                            <div class="team-role">{membro['cargo']}</div>
                            <div class="contact-container">
                                <a href="{link_whatsapp}" target="_blank" class="contact-link">
                                    <img src="{wa_icon_url}" class="whatsapp-icon"> {membro['telefone']}
                                </a>
                                <a href="mailto:{membro['email']}" class="contact-link">
                                    ✉️ {membro['email']}
                                </a>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
    
################################################################################
# --- MÓDULO 2: SIMULADOR DE BONIFICAÇÃO ---
################################################################################
elif aba_selecionada == "💰 Simulador de Bonificação":
    st.header("💰 Simulador de Bonificação Individual")
    
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
    
    # Criando 3 colunas para distribuir melhor os materiais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📁 Materiais de Venda")
        arquivos_venda = {
            "📖 Catálogo Digital (PDF)": "catalogo-papapa-digital.pdf",
            "💰 Tabela de Preços (Excel)": "Tabela de preços Papapá 0226 v2.xlsx",
            "🌿 Tabela de Preços - Mundo Verde": "Tabela de preços Papapá 0625 Mundo Verde.xlsx",
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
            "📝 Templates (PDF)": "Templates IS 2026.docx (2).pdf",
            "📊 Central de Templates Comercial": "Central de Templates Comercial - PAPAPÁ.xlsx",
            "🧩 Sales Planning Framework": "[PAPAPÁ] - Sales Planning Framework.xlsx"
        }
        for label, path in arquivos_proc.items():
            try:
                with open(path, "rb") as f:
                    st.download_button(label, f, file_name=path, use_container_width=True)
            except FileNotFoundError: st.error(f"Arquivo não encontrado: {path}")

    with col3:
        st.subheader("🏦 Documentos Fiscais")
        arquivos_fiscais = {
            "📄 Ata AGE 2025 (Sede/Matriz)": "2025_07_08, Baby Roo, Ata AGE 2025, mudança sede e matriz, versão JUCEPAR, WSA, Registrada.pdf",
            "✅ CND - Débitos Federais": "- CND – Certidão Negativa de Débitos Federais 1.pdf",
            "🏙️ CND - Débitos Municipais": "CND MUNICIPAL - BABY ROO.pdf",
            "👨‍🚒 Alvará Bombeiro (Venc. 11/2026)": "BABY ROO - CVCB Bombeiro - venc 04.11.2026.pdf",
            "💳 Cartão CNPJ": "CARTÃO CNPJ BABY ROO.pdf",
            "🏛️ Inscrição Municipal": "INSCRIÇÃO MUNICIPAL.pdf",
            "📑 Sintegra": "SINTEGRA PAPAPÁ.pdf",
            "💰 Comprovante Bancário": "COMPROVANTE BANCÁRIO (1).png"
        }
        for label, path in arquivos_fiscais.items():
            try:
                with open(path, "rb") as f:
                    # O streamlit identifica automaticamente se é PNG ou PDF pelo nome do arquivo no path
                    st.download_button(label, f, file_name=path, use_container_width=True)
            except FileNotFoundError: 
                st.error(f"Arquivo não encontrado: {path}")

        st.divider()

    # NOVO BLOCO: TELEFONES VEKTA
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
        "🔄 Recuperação"
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
        st.subheader("📊 Material de Apoio Completo")
        
        # O botão de download agora está corretamente identado dentro da tabs[4]
        nome_arquivo = "Central de Templates Comercial - PAPAPÁ.xlsx"
        try:
            with open(nome_arquivo, "rb") as file:
                st.download_button(
                    label="📥 Baixar Central de Templates Comercial (Completa)",
                    data=file,
                    file_name=nome_arquivo,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    help="Clique para baixar a planilha com todos os scripts de abordagem e recuperação."
                )
        except FileNotFoundError:
            st.error("Arquivo de templates não encontrado no diretório do servidor.")

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
        st.markdown("""
            <div class="unidade-row"><span class="unidade-nome">🍎 Papinhas de Fruta</span><span class="unidade-valor">16 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">👨‍🍳 La Chef</span><span class="unidade-valor">16 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">🍼 Yoguzinho</span><span class="unidade-valor">15 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">🦷 Dentição</span><span class="unidade-valor">15 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">🍝 Macarrão</span><span class="unidade-valor">14 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">🥣 Sopinhas</span><span class="unidade-valor">12 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">🥩 Papinhas de Carne</span><span class="unidade-valor">12 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">🌾 Cereal</span><span class="unidade-valor">12 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">🍪 Biscotti</span><span class="unidade-valor">10 meses</span></div>
            <div class="unidade-row"><span class="unidade-nome">🥖 Palitinhos</span><span class="unidade-valor">9 meses</span></div>
        """, unsafe_allow_html=True)
        st.caption("❄️ Nenhuma linha necessita de refrigeração.")

        st.write("") 

        # 2. UNIDADES POR CAIXA
        st.subheader("📦 Unidades por Caixa")
        st.markdown("""
            <div class="unidade-row"><span class="unidade-nome">🍼 Yoguzinho</span><span class="unidade-valor">16 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">🥖 Palitinhos</span><span class="unidade-valor">16 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">👨‍🍳 La Chef</span><span class="unidade-valor">6 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">🥣 Sopinhas</span><span class="unidade-valor">6 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">🍎 Papinhas de Fruta</span><span class="unidade-valor">12 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">🥩 Papinhas de Carne</span><span class="unidade-valor">12 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">🦷 Dentição</span><span class="unidade-valor">12 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">🍝 Macarrão</span><span class="unidade-valor">12 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">🌾 Cereal</span><span class="unidade-valor">12 un.</span></div>
            <div class="unidade-row"><span class="unidade-nome">🍪 Biscotti</span><span class="unidade-valor">12 un.</span></div>
        """, unsafe_allow_html=True)

    with col_info2:
        st.subheader("💳 Modalidades de Pagamento")
        
        st.markdown("""
            <style>
            .pagamento-texto { font-size: 16px; line-height: 1.6; color: #31333F; }
            .highlight { background-color: #f0f2f6; padding: 2px 6px; border-radius: 4px; font-weight: bold; }
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

        with st.expander("Prazos: Demais Regiões", expanded=True):
            st.markdown("""
            <div class="pagamento-texto">
            • <b>Até R$ 1.000:</b> <span class="highlight">45 dias</span><br>
            • <b>R$ 1.000 a R$ 2.000:</b> <span class="highlight">45/60 dias</span><br>
            • <b>Acima de R$ 2.000:</b> <span class="highlight">40/50/60 dias</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.success("**Pagamento:** Pix ou Boleto")

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
            
            # Carrega a planilha
            df_prazos = pd.read_excel("Tabela lead time operacao e comercial.xlsx")
            
            # Criamos a coluna formatada
            df_prazos['Exibicao'] = df_prazos['Cidade'].astype(str) + " (" + df_prazos['UF'].astype(str) + ")"
            opcoes_cidades = sorted(df_prazos['Exibicao'].unique())
            
            cid_sel = st.selectbox("Selecione a Cidade:", opcoes_cidades, label_visibility="collapsed")
            
            # BUSCA O VALOR E CONVERTE PARA INTEIRO PARA TIRAR O .0
            valor_raw = df_prazos[df_prazos['Exibicao'] == cid_sel]['Lead time total'].values[0]
            dias_est = int(valor_raw) # <--- A mágica acontece aqui
            
            st.markdown(f"""
                <div style="background-color: #e8f4f8; padding: 15px; border-radius: 10px; border-left: 5px solid #29b5e8; text-align: center;">
                    <span style="color: #1f77b4; font-size: 14px; font-weight: bold;">PREVISÃO TOTAL</span><br>
                    <span style="font-size: 24px; font-weight: bold; color: #31333F;">{dias_est} dias úteis</span>
                </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error("Erro ao carregar a tabela de prazos.")
            st.caption(f"Erro técnico: {e}")

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
            </div>
        """, unsafe_allow_html=True)

        # Prospecção e Qualificação
        st.markdown(f"""
            <div class="glossary-card" style="margin-top: 15px;">
                <div class="glossary-category">🔍 Prospecção & Qualificação</div>
                {item_glossario("SDR (Sales Development Rep)", "Profissional que prospecta leads iniciais e os qualifica.")}
                {item_glossario("BDR (Business Development Rep)", "Foco em expansão de negócios e novas contas estratégicas.")}
                {item_glossario("BANT", "Critério de qualificação (Budget, Authority, Need, Timeline).")}
                {item_glossario("Cold Call/Mail", "Contato inicial não solicitado para gerar interesse.")}
            </div>
        """, unsafe_allow_html=True)

        # Processo de Vendas
        st.markdown(f"""
            <div class="glossary-card" style="margin-top: 15px;">
                <div class="glossary-category">⚙️ Processo de Vendas</div>
                {item_glossario("MQL / SQL / SAL", "Estágios de qualificação do lead (Marketing, Vendas e Aceito).")}
                {item_glossario("Pipeline", "Visão das etapas do funil (prospecção até fechamento).")}
                {item_glossario("Ramp-up", "Período para um vendedor atingir produtividade plena.")}
            </div>
        """, unsafe_allow_html=True)

    with col2:
        # Logística e Identificação
        st.markdown(f"""
            <div class="glossary-card">
                <div class="glossary-category">📦 Logística & Identificação</div>
                {item_glossario("SKU (Stock Keeping Unit)", "Código interno alfanumérico único para gerenciar estoque.")}
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
                {item_glossario("Churn", "Taxa de perda de clientes ou cancelamentos.")}
            </div>
        """, unsafe_allow_html=True)

        # Outros Relevantes
        st.markdown(f"""
            <div class="glossary-card" style="margin-top: 15px;">
                <div class="glossary-category">🤝 Outros Relevantes</div>
                {item_glossario("Account", "Conta empresarial (cliente B2B recorrente).")}
                {item_glossario("Closer/Rep", "Vendedor responsável pelo fechamento final.")}
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
