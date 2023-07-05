import fastapi
from fastapi import Depends, security, HTTPException
from sqlalchemy import orm
from typing import List
from PIL import Image
import base64
from io import BytesIO
import email_validator as email_check
import passlib.hash as hash
import jwt as jwt
from .config import settings
from .configs.db import SessionLocal, Base, engine
from .models.index import Participante, Encaminhamento, Reuniao  , User as User_Model
from .schemas.index import  UserCreate, User as User_Schema, EncaminhamentoCreate, ReuniaoCreate, ParticipanteCreate

SECRET = settings.TOKEN_SECRET

oauth2schema = security.OAuth2PasswordBearer("/token")
def create_database():
    return Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_by_id(db: orm.Session, user_id: int):
    return db.query(User_Model).filter(User_Model.id == user_id).first()

def get_all_users(db: orm.Session):
    return db.query(User_Model).all()


def get_user_by_email(db: orm.Session, email: str):
    return db.query(User_Model).filter(User_Model.email == email).first()


def get_users(db: orm.Session, skip: int = 0, limit: int = 100):
    return db.query(User_Model).offset(skip).limit(limit).all()


async def create_user(db: orm.Session, user: UserCreate):
    try:
        valid = email_check.validate_email(email=user.email)
        email = valid.email
    except email_check.EmailNotValidError:
        raise fastapi.HTTPException(status_code=404, detail="Please enter a valid email!")


    hashed_password = hash.bcrypt.hash(user.password)
    db_user = User_Model(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: orm.Session, user_id: int, user: UserCreate):
    try:
        valid = email_check.validate_email(email=user.email)
        email = valid.email
    except email_check.EmailNotValidError:
        raise fastapi.HTTPException(status_code=404, detail="Please enter a valid email!")

    hashed_password = hash.bcrypt.hash(user.password)
    db_user = get_user_by_id(db=db, user_id=user_id)
    db_user.email = user.email
    db_user.hashed_password = hashed_password
    db.commit()
    db.refresh(db_user)
    return db_user

async def create_token(user: User_Model):
    user_schema_obj = User_Schema.from_orm(user)
    user_dict = user_schema_obj.dict()
    token = jwt.encode(user_dict, SECRET)

    return dict(access_token=token, token_type="bearer")

def authenticate_user(email: str, password: str, db: orm.Session):
    user_token = get_user_by_email(email=email, db=db)

    if not user_token:
        return False

    if not user_token.verify_password(password=password):
        return False

    return user_token


async def get_current_user(db: orm.Session = Depends(get_db), token: str = Depends(oauth2schema)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        user = db.query(User_Model).get(payload["id"])

    except:
        raise HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )
    return User_Schema.from_orm(user)


def get_all_encs(db: orm.Session):
    return db.query(Encaminhamento).all()

def get_enc_by_id(db: orm.Session, enc_id: int):
    return db.query(Encaminhamento).filter(Encaminhamento.id == enc_id).first()

def create_enc(encaminhamento: EncaminhamentoCreate, db: orm.Session):
    enc_dict = encaminhamento.dict()
    db_encaminhamento = Encaminhamento(**enc_dict)
                                        
    db.add(db_encaminhamento)
    db.commit()
    db.refresh(db_encaminhamento)
    return db_encaminhamento


def get_all_reunioes(db: orm.Session):
    return db.query(Reuniao).all()

def get_reuniao_by_id(db: orm.Session, reuniao_id: int):
    return db.query(Reuniao).filter(Reuniao.id == reuniao_id).first()

def create_reuniao(reuniao: ReuniaoCreate, db: orm.Session):
    reuniao_dict = reuniao.dict()
    bd_reuniao = Reuniao(**reuniao_dict)
    db.add(bd_reuniao)
    db.commit()
    db.refresh(bd_reuniao)
    return bd_reuniao

def add_reuniao_a_enc(db: orm.Session, encaminhamento: Encaminhamento, reuniao: Reuniao):
    encaminhamento.reunioes.append(reuniao)
    db.commit()

def get_all_parts(db: orm.Session):
    return db.query(Participante).all()

def create_participante(participante: ParticipanteCreate, db: orm.Session):
    part_dict = participante.dict()
    bd_part = Participante(**part_dict)
    db.add(bd_part)
    db.commit()
    db.refresh(bd_part)
    return bd_part