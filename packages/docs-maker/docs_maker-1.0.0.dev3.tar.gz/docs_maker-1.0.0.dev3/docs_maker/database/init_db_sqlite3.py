from docs_maker.database.base import IBase
from docs_maker.database.models import Documents

class InitDbSqlite3():
    def __init__(self, db_name: str):
        self.__db_name = db_name

    @property
    def db_name(self):
        return self.__db_name

    def init(self):
        iBase = IBase()
        engine = iBase.get_sqlite_engine(self.db_name)

        iBase.Base.metadata.create_all(engine)
        session = iBase.get_session(engine)

        session.close()
