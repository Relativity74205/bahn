from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DatabaseConnection:
    def __init__(self):
        self.url = self.set_url()
        self.engine = create_engine(self.url, echo=True)

    @staticmethod
    def set_url():
        # TODO
        url = 'sqlite:///:memory:'

        return url
