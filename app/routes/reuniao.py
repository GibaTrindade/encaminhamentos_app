from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy import orm
from ..configs.db import conn
from ..schemas.index import Reuniao
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




