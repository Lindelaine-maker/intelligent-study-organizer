"""
AIOE - Assistente Inteligente de Organização de Estudos
Módulo principal do projeto
"""

__version__ = "1.0.0"
__author__ = "Lindelaine-maker"

from .organizer import StudyOrganizer
from .scheduler import StudyScheduler

__all__ = ['StudyOrganizer', 'StudyScheduler']