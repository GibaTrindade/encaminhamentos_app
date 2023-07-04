from pydantic import BaseModel
from typing import TYPE_CHECKING, List


class ReuniaoBase(BaseModel):
    id: int
    nome: str

    class Config:
        orm_mode = True

class ReuniaoCreate(BaseModel):
    nome: str

    class Config:
        orm_mode = True





