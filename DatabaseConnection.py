from typing import List
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

import config.config as config


Base = declarative_base()


class DatabaseConnection:
    def __init__(self):
        self.db_config = config.DB_URL
        self.url = self._set_url()
        self.engine = create_engine(self.url, echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def _set_url(self):
        url = self.db_config['url']

        return url

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def drop_all(self):
        Base.metadata.drop_all(self.engine)

    def save_bulk(self, objects: List, obj_name: str):
        with self.error_handling():
            self.session.bulk_save_objects(objects)
            self.session.commit()
    #
    # def get_train_stop_from_db(train_stop_change: Dict) -> Optional[TrainStop]:
    #     return None

    @contextmanager
    def error_handling(self):
        try:
            yield
        except SQLAlchemyError as e:
            print(str(e))
            raise
