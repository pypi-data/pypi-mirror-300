from sqlalchemy.orm import Session
from docs_maker.database.base import IBase


class InitDbPostgres:
    import docs_maker.database.models

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

        return session

    @staticmethod
    def close_session(session: Session):
        session.close()
