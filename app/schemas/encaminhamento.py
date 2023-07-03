from pydantic import BaseModel
from typing import TYPE_CHECKING, List
from enum import Enum
#from .reuniao import ReuniaoBase

class Status(str, Enum):
    INICIADO = 'INICIADO'
    FINALIZADO = 'FINALIZADO'
    ATRASADO = 'ATRASADO'
    CANCELADO = 'CANCELADO'


class EncaminhamentoBase(BaseModel):
    id: int
    assunto: str
    tema: str
    observacao: str
    status: Status = None
    
    class Config:
        orm_mode = True

class EncaminhamentoCreate(EncaminhamentoBase):
    pass



