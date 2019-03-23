from typing import List
from contextlib import contextmanager

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

import config.config as config
from Base import Base


class DatabaseConnection:
    def __init__(self):
        self.db_config = config.DB_URL
        self.url = self._set_url()
        self.engine = create_engine(self.url, echo=False)
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
        msg = f'Bulk saving {len(objects)} {obj_name} objects;'
        with self.error_handling(msg):
            self.session.bulk_save_objects(objects)
            self.session.commit()

    @contextmanager
    def error_handling(self, msg):
        try:
            yield
        except SQLAlchemyError as e:
            print(f'SQLAlchemyError (type {type(e).__name__}) during : {msg}, Exception: {str(e)}')
            raise

    def get_by_pk(self, obj: object, pk_id):
        msg = f'Getting Object {obj.__name__} by PK {pk_id};'
        with self.error_handling(msg):
            result = self.session.query(obj).get(pk_id)

        return result
