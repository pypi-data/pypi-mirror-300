from sqlalchemy import Column, Integer, String
from docs_maker.database.base import IBase

class Documents2(IBase.Base):
    __tablename__ = 'documents2'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
