# Models module for processos app
from .base import BaseModel
from .agenda import Agenda
from .constants import *

__all__ = [
    'BaseModel',
    'Agenda',
    # Constants
    'PROCESSO_STATUS_CHOICES',
    'PROCESSO_TIPOS_CHOICES',
    'MIN_PRIORIDADE',
    'MAX_PRIORIDADE',
    'MIN_VAGAS',
    'MAX_VAGAS',
] 