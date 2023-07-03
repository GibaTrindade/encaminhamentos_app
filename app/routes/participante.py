from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy import orm
from ..services import get_db, get_all_parts
from ..schemas.index import Participante

participante = APIRouter()


@participante.get("/participantes", response_model=List[Participante], tags=["participante"])
async def read_data(db: orm.Session=Depends(get_db)):
    #if Current User is admin, return all aircrafts
    #if cur_user.is_admin:
    #    return get_all_aircrafts(db=db)

    #if Current User is not admin, return only its aircrafts
    
    #enc_list = []
    part_list = get_all_parts(db=db)
    #print(enc_list)
    #businesses = get_business_by_user_id(user_id=cur_user.id, db=db


    return part_list


