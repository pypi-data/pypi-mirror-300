from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

class IBase():
    Base = declarative_base()

    # Нужны сторонние библиотеки для дружбы с java. Реализация на потом.
    # def get_h2_engine(self, db_name):
    #     return create_engine(f'h2+zxjdbc:///{db_name}', echo=True)

    def get_pg_engine(self, username, password, hostname, db_port, db_name):
        return create_engine(f'postgresql+psycopg2://{username}:{password}@{hostname}:{db_port}/{db_name}', echo=True)

    def get_sqlite_engine(self, db_name):
        return create_engine(f'sqlite:///{db_name}', echo=True)

    def get_session(self, engine):
        Session = sessionmaker(bind=engine)
        return Session()