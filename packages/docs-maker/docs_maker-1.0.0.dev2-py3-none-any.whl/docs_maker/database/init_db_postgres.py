from docs_maker.database.base import IBase
from docs_maker.database.models import Documents

class InitDbPostgres():
    def __init__(self, username: str, password: str, hostname: str, port: str, db_name: str):
        self.__username = username
        self.__password = password
        self.__hostname = hostname
        self.__port = port
        self.__db_name = db_name

    def init(self):
        iBase = IBase()

        engine = iBase.get_pg_engine(self.__username, self.__password, self.__hostname, self.__port, self.__db_name)

        iBase.Base.metadata.create_all(engine)
        session = iBase.get_session(engine)

        session.close()
