# Models module for processos app
from .agenda import Agenda
from .base import BaseModel
from .constants import MODALIDADE_CHOICES

__all__ = [
    "BaseModel",
    "Agenda",
    # Constants
    "MODALIDADE_CHOICES",
]
