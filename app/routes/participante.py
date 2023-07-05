from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy import orm
from ..services import get_db, get_all_parts, create_participante
from ..schemas.index import Participante, ParticipanteCreate, ParticipanteBase

participante = APIRouter()


@participante.get("/participantes/", response_model=List[Participante], tags=["participante"]) #response_model=List[Participante],
async def read_data(db: orm.Session=Depends(get_db)):
    part_list = get_all_parts(db=db)

    return part_list

@participante.post("/participante/", response_model=Participante,  tags=["participante"]) #response_model=Participante,
def criar_participante(participante: ParticipanteCreate, db: orm.Session = Depends(get_db)):
    db_participante: ParticipanteCreate = create_participante(participante, db)
    return db_participante
