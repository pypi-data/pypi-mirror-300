from sqlalchemy import Column, Integer, String
from docs_maker.database.base import IBase

class Configurations(IBase.Base):
    __tablename__ = 'configurations'

    id = Column(Integer, primary_key=True)
    config_key = Column(String)
    config_value = Column(String)
