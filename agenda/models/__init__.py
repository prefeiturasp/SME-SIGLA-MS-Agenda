# Models module for processos app
from .base import BaseModel
from .agenda import Agenda
from .constants import *

__all__ = [
    'BaseModel',
    'Agenda',
    # Constants
    'MODALIDADE_CHOICES',
] 