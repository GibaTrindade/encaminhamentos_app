from .reuniao import ReuniaoBase
from .encaminhamento import EncaminhamentoBase
from typing import TYPE_CHECKING, List


class Encaminhamento(EncaminhamentoBase):
    id: int
    reunioes: List[ReuniaoBase]

