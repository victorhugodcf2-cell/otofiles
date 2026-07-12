import streamlit as st
import datetime

# Configuração inicial da página para mobile e desktop
st.set_page_config(
    page_title="OtoFiles",
    page_icon="👂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização em CSS para deixar a interface limpa e profissional para ambiente clínico
st.markdown("""
    <style>
    .main { 
        background-color: #f8f9fa; 
    }
    .stButton>button { 
        width: 100%; 
        background-color: #0b57d0; 
        color: white; 
        border-radius: 8px;
    }
    .patient-card { 
        padding: 16px; 
        border-radius: 12px; 
        background-color: white; 
        border-left: 5px solid #0b57d0; 
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Simulamos um banco de dados temporário na memória do navegador (st.session_state)
# futuramente ele será conectado a um banco de dados real (como o Supabase)
if 'pacientes' not in st.session_state:
    st.session_state.pacientes = [
        {"id": "102938", "nome": "João Silva"},
        {"id": "456789", "nome": "Maria Oliveira"}
    ]

if 'videos' not in st.session_state:
    st.session_state.videos = [
        {
            "paciente_id": "102938", 
            "data": "2026-05-10", 
            "lado": "Orelha Direita (OD)", 
            "url": "https://www.w3schools.com/html/mov_bbb.mp4"
        },
        {
            "paciente_id": "102938", 
            "data": "2026-05-10", 
            "lado": "Orelha Esquerda (OE)", 
            "url": "https://www.w3schools.com/html/movie.mp4"
        },
        {
            "paciente_id": "456789", 
            "data": "2026-06-01", 
            "lado": "Orelha Direita (OD)", 
            "url": "https://www.w3schools.com/html/mov_bbb.mp4"
        }
    ]

# Título principal do aplicativo
st.title("👂 OtoFiles")
st.caption("Residência de Otorrinolaringologia — Arquivo Digital de Otoscopias")

# Criação das abas de navegação da tela inicial
tab_busca, tab_cadastro = st.tabs(["🔍 Buscar Paciente", "➕ Cadastrar Novo Paciente"])

with tab_busca:
    busca = st.text_input(
        "Digite o Nome ou o Prontuário do paciente:", 
        placeholder="Ex: João Silva ou 102938"
    ).strip()
    
    if busca:
        # Filtragem em tempo real por nome ou número do prontuário
        resultados = [
            p for p in st.session_state.pacientes 
            if busca.lower() in p['nome'].lower() or busca in p['id']
        ]
        
        if resultados:
            st.subheader(f"Resultados encontrados ({len(resultados)}):")
            for p in resultados:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(
                        f"<div class='patient-card'><b>{p['nome']}</b><br>Prontuário: {p['id']}</div>", 
                        unsafe_allow_html=True
                    )
                with col2:
                    # Botão para abrir o perfil do paciente correspondente
                    if st.button("Ver Perfil", key=f"btn_{p['id']}"):
                        st.session_state.paciente_atual = p
        else:
            st.error("Nenhum paciente cadastrado com esses dados.")

with tab_cadastro:
    st.subheader("Novo Registro de Paciente")
    novo_nome = st.text_input("Nome Completo do Paciente", placeholder="Ex: Carlos Eduardo de Souza")
    novo_id = st.text_input("Número do Prontuário / Registro Hospitalar", placeholder="Ex: 789123")
    
    if st.button("Salvar Paciente"):
        if novo_nome and novo_id:
            # Garante que o prontuário seja único no sistema
            if any(p['id'] == novo_id for p in st.session_state.pacientes):
                st.warning("Este número de prontuário já está cadastrado.")
            else:
                st.session_state.pacientes.append({"id": novo_id, "nome": novo_nome})
                st.success(f"Paciente {novo_nome} cadastrado com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos obrigatórios.")

# Se o usuário clicou para ver o perfil de um paciente, renderizamos a tela dele
if 'paciente_atual' in st.session_state:
    p = st.session_state.paciente_atual
    st.write("---")
    
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("⬅️ Voltar"):
            del st.session_state.paciente_atual
            st.rerun()
            
    st.header(f"👤 {p['nome']}")
    st.info(f"**Número de Registro/Prontuário:** {p['id']}")
    
    # Seção colapsável de Upload de Novos Vídeos
    with st.expander("🎥 Fazer Upload de Nova Otoscopia", expanded=False):
        col_data, col_lado = st.columns(2)
        with col_data:
            data_exame = st.date_input("Data do Exame", datetime.date.today())
        with col_lado:
            lado_exame = st.selectbox("Lateralidade", ["Orelha Direita (OD)", "Orelha Esquerda (OE)"])
            
        video_file = st.file_uploader(
            "Selecione o vídeo da otoscopia (Formatos aceitos: MP4, MOV)", 
            type=["mp4", "mov", "avi"]
        )
        
        if st.button("🚀 Salvar Exame"):
            if video_file is not None:
                # Na versão final conectada à nuvem, esse arquivo será enviado ao Storage do Supabase
                # Para o protótipo, simulamos adicionando à lista com um vídeo de exemplo padrão
                st.session_state.videos.append({
                    "paciente_id": p['id'],
                    "data": str(data_exame),
                    "lado": lado_exame,
                    "url": "https://www.w3schools.com/html/mov_bbb.mp4"
                })
                st.success("Vídeo de otoscopia salvo com sucesso!")
                st.rerun()
            else:
                st.error("Selecione um arquivo de vídeo antes de salvar.")

    # Exibição do histórico organizado por data e lateralidade
    st.subheader("📁 Histórico de Otoscopias")
    
    videos_paciente = [v for v in st.session_state.videos if v['paciente_id'] == p['id']]
    
    if not videos_paciente:
        st.write("Nenhum registro de vídeo anexado a este paciente.")
    else:
        # Agrupa os exames pelas datas existentes, mostrando os mais recentes primeiro
        datas = sorted(list(set([v['data'] for v in videos_paciente])), reverse=True)
        
        for data in datas:
            data_formatada = datetime.datetime.strptime(data, '%Y-%m-%d').strftime('%d/%m/%Y')
            st.markdown(f"#### 📅 Exames realizados em: {data_formatada}")
            
            videos_do_dia = [v for v in videos_paciente if v['data'] == data]
            col_od, col_oe = st.columns(2)
            
            for v in videos_do_dia:
                if "Direita" in v['lado']:
                    with col_od:
                        st.markdown("**🟢 Orelha Direita (OD)**")
                        st.video(v['url'])
                else:
                    with col_oe:
                        st.markdown("**🔵 Orelha Esquerda (OE)**")
                        st.video(v['url'])
            st.markdown("---")