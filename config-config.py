"""Configurações do AIOE"""

# Configurações da Aplicação
APP_NAME = "AIOE - Assistente Inteligente de Organização de Estudos"
APP_VERSION = "1.0.0"

# Configurações de Estudo
DEFAULT_STUDY_HOURS = 3
MAX_STUDY_HOURS = 8
MIN_STUDY_HOURS = 1

DIFFICULTY_LEVELS = {
    1: "Muito Fácil",
    2: "Fácil",
    3: "Médio",
    4: "Difícil",
    5: "Muito Difícil"
}

PRIORITY_LEVELS = {
    "Baixa": 1,
    "Média": 2,
    "Alta": 3
}

# Configurações de Banco de Dados
DATABASE_PATH = "data/study_organizer.db"

# Configurações de Interface
STREAMLIT_THEME = "light"
PAGE_ICON = "📚"

# Configurações de Agendamento
SCHEDULE_DAYS = 7
SCHEDULE_START_HOUR = 18  # 18:00 (6 PM)
SCHEDULE_END_HOUR = 22    # 22:00 (10 PM)

# Configurações de Tarefas
URGENT_TASK_THRESHOLD = 7  # dias até o prazo para considerar urgente