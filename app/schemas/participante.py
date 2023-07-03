from pydantic import BaseModel
from typing import TYPE_CHECKING, List
#from .reuniao import ReuniaoBase



class ParticipanteBase(BaseModel):
    id: int
    nome: str
    lotacao: str
    matricula: str
    
    class Config:
        orm_mode = True

class EncaminhamentoCreate(ParticipanteBase):
    pass




