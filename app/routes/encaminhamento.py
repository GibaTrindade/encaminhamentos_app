from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy import orm
from ..services import get_db, get_all_encs, create_enc
from ..schemas.index import Encaminhamento, EncaminhamentoCreate
from ..models.index import Encaminhamento as BD_Encaminhamento, Reuniao as BD_Reuniao

enc = APIRouter()


@enc.get("/enc", response_model=List[Encaminhamento], tags=["encaminhamento"])
async def read_data(db: orm.Session=Depends(get_db)):
    #if Current User is admin, return all aircrafts
    #if cur_user.is_admin:
    #    return get_all_aircrafts(db=db)

    #if Current User is not admin, return only its aircrafts
    
    #enc_list = []
    enc_list = get_all_encs(db=db)
    #print(enc_list)
    #businesses = get_business_by_user_id(user_id=cur_user.id, db=db


    return enc_list



@enc.post("/encaminhamentos/", response_model=Encaminhamento, tags=["encaminhamento"])
def criar_encaminhamento(encaminhamento: EncaminhamentoCreate, db: orm.Session = Depends(get_db)):
    db_encaminhamento = create_enc(encaminhamento, db)
    return db_encaminhamento

@enc.post("/reunioes/{reuniao_id}/adicionar_encaminhamento/{encaminhamento_id}")
def adicionar_encaminhamento(reuniao_id: int, encaminhamento_id: int, db: orm.Session = Depends(get_db)):
    reuniao: BD_Reuniao = db.query(BD_Reuniao).filter(BD_Reuniao.id == reuniao_id).first()
    encaminhamento = db.query(BD_Encaminhamento).filter(BD_Encaminhamento.id == encaminhamento_id).first()
    if not reuniao or not encaminhamento:
        raise HTTPException(status_code=404, detail="Reunião ou encaminhamento não encontrado.")
    reuniao.encaminhamentos.append(encaminhamento)
    db.commit()
    return {"message": "Encaminhamento adicionado à reunião com sucesso."}

