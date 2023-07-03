from .reuniao import ReuniaoBase
from .participante import ParticipanteBase
from typing import TYPE_CHECKING, List


class Participante(ParticipanteBase):
    reunioes: List[ReuniaoBase]
