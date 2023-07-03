from pydantic import BaseModel
from typing import TYPE_CHECKING, List
#from .encaminhamento import EncaminhamentoBase


class ReuniaoBase(BaseModel):
    id: int
    nome: str

    class Config:
        orm_mode = True

class ReuniaoCreate(ReuniaoBase):
    pass





