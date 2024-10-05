from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


class Database:
    Base = declarative_base()

    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def create_all(self):
        self.Base.metadata.create_all(self.engine)


DB = Database
