
import streamlit as st
import datetime
import time

# Configuração inicial da página para mobile e desktop
st.set_page_config(
    page_title="OtoFiles",
    page_icon="👂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização em CSS para deixar a interface limpa, moderna e amigável para celular/tablet
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
        border: none;
        padding: 8px 16px;
    }
    .stButton>button:hover {
        background-color: #0842a0;
        color: white;
    }
    .patient-card { 
        padding: 16px; 
        border-radius: 12px; 
        background-color: white; 
        border-left: 5px solid #0b57d0; 
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .delete-btn>button {
        background-color: #dc3545 !important;
        color: white !important;
    }
    .delete-btn>button:hover {
        background-color: #bb2d3b !important;
    }
    </style>
""", unsafe_allow_html=True)

# Inicialização do banco de dados temporário (st.session_state)
if 'pacientes' not in st.session_state:
    # Adicionamos um campo 'ultimo_acesso' para controlar a ordenação dos últimos vistos
    st.session_state.pacientes = [
        {"id": "102938", "nome": "João Silva", "ultimo_acesso": 1.0},
        {"id": "456789", "nome": "Maria Oliveira", "ultimo_acesso": 2.0}
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

# Título do Sistema
st.title("👂 OtoFiles")
st.caption("Residência de Otorrinolaringologia — Arquivo Digital de Otoscopias")

# Se o usuário NÃO estiver visualizando o perfil de um paciente, mostra a tela inicial
if 'paciente_atual' not in st.session_state:
    
    # Criação das três abas de controle principal
    tab_busca, tab_cadastro, tab_excluir = st.tabs([
        "🔍 Buscar/Listar Pacientes", 
        "➕ Cadastrar Novo Paciente", 
        "❌ Excluir Paciente"
    ])

    with tab_busca:
        # Barra de pesquisa
        busca = st.text_input(
            "Pesquisar paciente por Nome ou Prontuário:", 
            placeholder="Digite algo para filtrar ou deixe em branco para ver todos..."
        ).strip()
        
        # Ordena a lista de pacientes colocando os últimos acessados/vistos primeiro
        pacientes_ordenados = sorted(
            st.session_state.pacientes, 
            key=lambda x: x.get('ultimo_acesso', 0), 
            reverse=True
        )
        
        # Filtragem em tempo real
        if busca:
            resultados = [
                p for p in pacientes_ordenados 
                if busca.lower() in p['nome'].lower() or busca in p['id']
            ]
        else:
            resultados = pacientes_ordenados

        # Exibição da lista
        if resultados:
            st.subheader("Pacientes Cadastrados (Últimos vistos primeiro):")
            for p in resultados:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(
                        f"<div class='patient-card'><b>{p['nome']}</b><br>Prontuário: {p['id']}</div>", 
                        unsafe_allow_html=True
                    )
                with col2:
                    if st.button("Ver Perfil", key=f"ver_{p['id']}"):
                        # Atualiza o timestamp de último acesso do paciente selecionado
                        for pac in st.session_state.pacientes:
                            if pac['id'] == p['id']:
                                pac['ultimo_acesso'] = time.time()
                        st.session_state.paciente_atual = p
                        st.rerun()
        else:
            st.info("Nenhum paciente cadastrado ou encontrado com este critério de busca.")

    with tab_cadastro:
        st.subheader("Novo Registro de Paciente")
        novo_nome = st.text_input("Nome Completo do Paciente", placeholder="Ex: Carlos Eduardo de Souza")
        novo_id = st.text_input("Número do Prontuário / Registro Hospitalar", placeholder="Ex: 789123")
        
        if st.button("Salvar e Abrir Perfil"):
            if novo_nome and novo_id:
                # Garante que o prontuário seja único
                if any(p['id'] == novo_id for p in st.session_state.pacientes):
                    st.warning("Este número de prontuário já está cadastrado no sistema.")
                else:
                    novo_paciente = {
                        "id": novo_id, 
                        "nome": novo_nome, 
                        "ultimo_acesso": time.time()
                    }
                    st.session_state.pacientes.append(novo_paciente)
                    
                    # Abre o perfil do novo paciente de forma imediata
                    st.session_state.paciente_atual = novo_paciente
                    st.success(f"Paciente {novo_nome} cadastrado! Abrindo o perfil...")
                    time.sleep(1) # Pequena pausa para o usuário ler a mensagem de sucesso
                    st.rerun()
            else:
                st.error("Por favor, preencha o Nome e o Prontuário para poder salvar.")

    with tab_excluir:
        st.subheader("Remover Paciente do Sistema")
        st.warning("Atenção: A exclusão de um paciente removerá também todo o histórico de otoscopias dele.")
        
        if not st.session_state.pacientes:
            st.write("Nenhum paciente cadastrado no momento.")
        else:
            # Lista suspensa com todos os pacientes para selecionar quem excluir
            opcoes_exclusao = {f"{p['nome']} (Prontuário: {p['id']})": p['id'] for p in st.session_state.pacientes}
            paciente_para_excluir_label = st.selectbox("Selecione o paciente que deseja excluir:", list(opcoes_exclusao.keys()))
            id_para_excluir = opcoes_exclusao[paciente_para_excluir_label]
            
            # Botão destacado em vermelho (usando classe CSS personalizada)
            st.markdown("<div class='delete-btn'>", unsafe_allow_html=True)
            confirmado = st.button("Confirmar Exclusão Definitiva", key="btn_confirmar_exclusao")
            st.markdown("</div>", unsafe_allow_html=True)
            
            if confirmado:
                # Remove o paciente da lista
                st.session_state.pacientes = [p for p in st.session_state.pacientes if p['id'] != id_para_excluir]
                # Remove os vídeos vinculados a este paciente
                st.session_state.videos = [v for v in st.session_state.videos if v['paciente_id'] != id_para_excluir]
                
                st.success("Paciente e vídeos removidos com sucesso!")
                time.sleep(1)
                st.rerun()

# --- TELA DE PERFIL DO PACIENTE SELECIONADO ---
else:
    p = st.session_state.paciente_atual
    
    col_back, col_space = st.columns([1, 5])
    with col_back:
        if st.button("⬅️ Voltar"):
            del st.session_state.paciente_atual
            st.rerun()
            
    st.header(f"👤 {p['nome']}")
    st.info(f"**Número de Registro/Prontuário:** {p['id']}")
    
    # Seção colapsável de Upload de Novos Vídeos
    with st.expander("🎥 Fazer Upload de Nova Otoscopia", expanded=True):
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
                # Para o protótipo, adicionamos à lista simulando o upload
                st.session_state.videos.append({
                    "paciente_id": p['id'],
                    "data": str(data_exame),
                    "lado": lado_exame,
                    "url": "https://www.w3schools.com/html/mov_bbb.mp4" # Vídeo modelo temporário
                })
                st.success("Vídeo de otoscopia salvo com sucesso!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Selecione um arquivo de vídeo antes de clicar em salvar.")

    # Exibição do histórico organizado por data e lateralidade
    st.subheader("📁 Histórico de Otoscopias")
    
    videos_paciente = [v for v in st.session_state.videos if v['paciente_id'] == p['id']]
    
    if not videos_paciente:
        st.write("Nenhum registro de vídeo anexado a este paciente ainda.")
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
```
eof

### O que fazer para corrigir no seu GitHub:

1. Vá até o seu repositório no **GitHub** e clique em editar o arquivo (seja ele `app.py` ou `otofiles_app.py`, use o que você configurou).
2. **Apague todo o código que está lá atualmente**.
3. Copie o bloco acima e cole-o no arquivo. (Atenção: comece copiando da linha `import streamlit as st` até o final do arquivo, sem as tags pretas de formatação).
4. Salve as alterações clicando em **"Commit changes"**.

Em menos de um minuto, o seu aplicativo online estará no ar e sem erros de sintaxe! Se precisar de qualquer outra alteração, estou aqui.
