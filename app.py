import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from src.organizer import StudyOrganizer
from src.scheduler import StudyScheduler

# Configure page
st.set_page_config(
    page_title="Assistente Inteligente de Organização de Estudos",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'organizer' not in st.session_state:
    st.session_state.organizer = StudyOrganizer()

if 'scheduler' not in st.session_state:
    st.session_state.scheduler = StudyScheduler()

# Sidebar navigation
st.sidebar.title("📚 AIOE - Menu")
page = st.sidebar.radio(
    "Selecione uma opção:",
    ["🏠 Início", "📖 Cadastrar Disciplinas", "📝 Adicionar Tarefas", "📅 Ver Cronograma", "📊 Estatísticas"]
)

# Main content
if page == "🏠 Início":
    st.title("🎓 Assistente Inteligente de Organização de Estudos")
    st.markdown("""
    ### Bem-vindo ao AIOE!
    
    Este aplicativo foi desenvolvido para ajudar você a:
    - ✅ Organizar suas disciplinas e tarefas
    - ✅ Criar cronogramas inteligentes de estudo
    - ✅ Gerenciar seus prazos de forma eficiente
    - ✅ Melhorar seu desempenho acadêmico
    
    ### Como usar:
    1. **Cadastre suas disciplinas** na seção "Cadastrar Disciplinas"
    2. **Adicione suas tarefas** com prazos na seção "Adicionar Tarefas"
    3. **Visualize seu cronograma** na seção "Ver Cronograma"
    
    ### Dicas:
    - Quanto maior a dificuldade de uma disciplina, mais tempo será alocado para ela
    - Tarefas com maior prioridade serão agendadas primeiro
    - Você pode gerar um novo cronograma quantas vezes quiser
    
    Comece agora clicando em uma das opções no menu à esquerda! 🚀
    """)

elif page == "📖 Cadastrar Disciplinas":
    st.title("📖 Cadastrar Disciplinas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        disciplina = st.text_input("Nome da Disciplina:", key="disciplina_input")
    
    with col2:
        dificuldade = st.select_slider(
            "Nível de Dificuldade:",
            options=[1, 2, 3, 4, 5],
            value=3,
            format_func=lambda x: {1: "Muito Fácil", 2: "Fácil", 3: "Médio", 4: "Difícil", 5: "Muito Difícil"}[x]
        )
    
    if st.button("➕ Adicionar Disciplina", key="add_discipline"):
        try:
            st.session_state.organizer.add_discipline(disciplina, dificuldade)
            st.success(f"✅ Disciplina '{disciplina}' adicionada com sucesso!")
        except ValueError as e:
            st.error(f"❌ Erro: {str(e)}")
    
    # Display disciplines
    st.subheader("Disciplinas Cadastradas:")
    disciplines = st.session_state.organizer.get_disciplines()
    
    if disciplines:
        df = pd.DataFrame([
            {
                'ID': d['id'],
                'Nome': d['name'],
                'Dificuldade': {1: "Muito Fácil", 2: "Fácil", 3: "Médio", 4: "Difícil", 5: "Muito Difícil"}[d['difficulty']],
                'Data de Criação': d['created_at'][:10]
            }
            for d in disciplines
        ])
        st.dataframe(df, use_container_width=True)
        
        # Delete option
        with st.expander("🗑️ Remover Disciplina"):
            discipline_to_delete = st.selectbox(
                "Selecione a disciplina a remover:",
                options=disciplines,
                format_func=lambda x: x['name']
            )
            if st.button("Remover"):
                st.session_state.organizer.delete_discipline(discipline_to_delete['id'])
                st.success("Disciplina removida com sucesso!")
                st.rerun()
    else:
        st.info("Nenhuma disciplina cadastrada ainda.")

elif page == "📝 Adicionar Tarefas":
    st.title("📝 Adicionar Tarefas")
    
    disciplines = st.session_state.organizer.get_disciplines()
    
    if not disciplines:
        st.warning("⚠️ Cadastre disciplinas antes de adicionar tarefas!")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            disciplina_idx = st.selectbox(
                "Selecione a Disciplina:",
                options=range(len(disciplines)),
                format_func=lambda x: disciplines[x]['name']
            )
            disciplina = disciplines[disciplina_idx]
            tarefa = st.text_input("Descrição da Tarefa:")
        
        with col2:
            data_entrega = st.date_input("Data de Entrega:")
            prioridade = st.select_slider(
                "Prioridade:",
                options=[1, 2, 3, 4, 5],
                value=3,
                format_func=lambda x: {1: "Baixa", 2: "Média-Baixa", 3: "Média", 4: "Média-Alta", 5: "Alta"}[x]
            )
        
        if st.button("➕ Adicionar Tarefa", key="add_task"):
            try:
                st.session_state.organizer.add_task(
                    disciplina['id'],
                    tarefa, 
                    data_entrega, 
                    prioridade
                )
                st.success("✅ Tarefa adicionada com sucesso!")
            except ValueError as e:
                st.error(f"❌ Erro: {str(e)}")
        
        # Display tasks
        st.subheader("Tarefas Cadastradas:")
        tasks = st.session_state.organizer.get_tasks()
        
        if tasks:
            df = pd.DataFrame([
                {
                    'ID': t['id'],
                    'Disciplina': t['discipline_name'],
                    'Tarefa': t['description'],
                    'Data': t['due_date'],
                    'Prioridade': {1: "Baixa", 2: "Média-Baixa", 3: "Média", 4: "Média-Alta", 5: "Alta"}[t['priority']],
                    'Status': "✅ Completa" if t['completed'] else "⏳ Pendente"
                }
                for t in tasks
            ])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhuma tarefa cadastrada ainda.")

elif page == "📅 Ver Cronograma":
    st.title("📅 Ver Cronograma de Estudos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        tempo_diario = st.number_input(
            "Horas disponíveis por dia:",
            min_value=1.0,
            max_value=12.0,
            value=4.0,
            step=0.5
        )
    
    with col2:
        hora_inicio = st.time_input("Hora de início dos estudos:", value=datetime.strptime("18:00", "%H:%M").time())
    
    if st.button("📊 Gerar Cronograma", key="generate_schedule"):
        tasks = st.session_state.organizer.get_pending_tasks()
        disciplines = st.session_state.organizer.get_disciplines()
        
        if not tasks or not disciplines:
            st.warning("⚠️ Cadastre disciplinas e tarefas antes de gerar o cronograma!")
        else:
            schedule = st.session_state.scheduler.generate_schedule(
                tasks, 
                disciplines, 
                tempo_diario, 
                hora_inicio
            )
            
            st.success("✅ Cronograma gerado com sucesso!")
            st.subheader("Seu Cronograma Semanal:")
            
            for day in st.session_state.scheduler.days_of_week:
                activities = schedule.get(day, [])
                if activities:
                    st.markdown(f"### {day}")
                    for activity in activities:
                        st.markdown(f"**{activity['time']} - {activity['end_time']}** | {activity['discipline']}")
                        st.markdown(f"> {activity['task']}")
                else:
                    st.markdown(f"### {day}")
                    st.markdown("Sem atividades agendadas")

elif page == "📊 Estatísticas":
    st.title("📊 Estatísticas de Estudos")
    
    stats = st.session_state.organizer.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Disciplinas", stats['total_disciplines'])
    
    with col2:
        st.metric("Total de Tarefas", stats['total_tasks'])
    
    with col3:
        st.metric("Tarefas Pendentes", stats['pending_tasks'])
    
    with col4:
        st.metric("Tarefas Completas", stats['completed_tasks'])
    
    st.subheader("Dificuldade Média das Disciplinas")
    st.metric("Dificuldade Média", f"{stats['average_difficulty']:.1f}/5")