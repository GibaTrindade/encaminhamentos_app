from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy import orm
from ..configs.db import conn
from ..schemas.index import Reuniao, ReuniaoCreate
from ..models.index import Reuniao as BD_Reuniao
from ..models.index import Encaminhamento as BD_Encaminhamento
from ..services import get_db, get_all_reunioes
import json

reuniao = APIRouter()

#response_model=List[Reuniao],
@reuniao.get("/reuniao", response_model=List[Reuniao], tags=["reuniao"])
async def read_data(db: orm.Session=Depends(get_db)):
    db_reuniao = get_all_reunioes(db=db)
    return db_reuniao


#@reuniao.get("/reuniao/{id}", tags=["reuniao"])
#async def read_data(id: int, db: orm.Session=Depends(get_db)):
#    return get_reuniao_by_id(db=db, reuniao_id=id)


@reuniao.post("/reunioes/", response_model=Reuniao, tags=["reuniao"])
def criar_reuniao(reuniao: ReuniaoCreate, db: orm.Session = Depends(get_db)):
    bd_reuniao = BD_Reuniao(nome = reuniao.nome)
    db.add(bd_reuniao)
    db.commit()
    db.refresh(bd_reuniao)
    return bd_reuniao

@reuniao.post("/encaminhamento/{encaminhamento_id}/adicionar_reuniao/{reuniao_id}")
def adicionar_encaminhamento(reuniao_id: int, encaminhamento_id: int, db: orm.Session = Depends(get_db)):
    reuniao: BD_Reuniao = db.query(BD_Reuniao).filter(BD_Reuniao.id == reuniao_id).first()
    encaminhamento: BD_Encaminhamento = db.query(BD_Encaminhamento).filter(BD_Encaminhamento.id == encaminhamento_id).first()
    if not reuniao or not encaminhamento:
        raise HTTPException(status_code=404, detail="Reunião ou encaminhamento não encontrado.")
    encaminhamento.reunioes.append(reuniao)
    db.commit()
    return {"message": "Reunão adicionada ao encaminhamento com sucesso."}