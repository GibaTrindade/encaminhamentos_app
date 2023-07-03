from sqlalchemy import Table, Column, ForeignKey
from ..configs.db import Base

part_reunioes = Table('part_reunioes', Base.metadata,
    Column('part_id', ForeignKey('participantes.id'), primary_key=True),
    Column('reuniao_id', ForeignKey('reunioes.id'), primary_key=True)
)
    
