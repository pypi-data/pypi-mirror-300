from sqlalchemy.orm import Session
from docs_maker.database.base import IBase


class InitDbSqlite3:
    import docs_maker.database.models

    def __init__(self, db_name: str):
        self.__db_name = db_name
        self.iBase = IBase()
        self.engine = self.iBase.get_sqlite_engine(self.db_name)

    @property
    def db_name(self):
        return self.__db_name

    def init(self):
        self.iBase.Base.metadata.create_all(self.engine)
        session = self.iBase.get_session(self.engine)

        return session

    @staticmethod
    def close_session(session: Session):
        session.close()
