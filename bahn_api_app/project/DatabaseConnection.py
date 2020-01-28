from typing import List
from contextlib import contextmanager

from sqlalchemy import create_engine, func, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

import config.config as config
from project.Base import Base
from project.TrainStopChange import TrainStopChange
from project.TrainStop import TrainStop


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
        msg = f'Error while writing bulk saving {len(objects)} {obj_name} objects;'
        with self.error_handling(msg):
            self.session.bulk_save_objects(objects)
            self.session.commit()
        # TODO create fallback function (instead of bulk insert, insert single line and looking before)
        # if 'constraint failed' in str(e):
        #     logging.critical('At least one dataset already in DB, switching to fallback')

    @contextmanager
    def error_handling(self, msg):
        try:
            yield
        except SQLAlchemyError as e:
            msg = f'SQLAlchemyError (type {type(e).__name__}) during : {msg}, Exception: {str(e)}'
            raise SQLAlchemyError(msg)

    def get_by_pk(self, obj: object, pk_id):
        msg = f'Getting Object {obj.__name__} by PK {pk_id};'
        with self.error_handling(msg):
            result = self.session.query(obj).get(pk_id)

        return result

    def get_last_tstamp_request(self, station: str, request_type: str = None):
        msg = f'Error when getting last_tstamp_request for station {station} and request_type {request_type}.'
        with self.error_handling(msg):
            if request_type:
                result = (self.session
                          .query(func.max(TrainStopChange.tstamp_request))
                          .filter(and_(TrainStopChange.request_type == request_type, TrainStopChange.station == station))
                          .scalar())
            else:
                result = (self.session
                          .query(func.max(TrainStopChange.tstamp_request))
                          .filter(TrainStopChange.station == station)
                          .scalar())

        return result

    def get_last_datehour_default_plan(self, station: str):
        msg = f'Error when getting last datehour default_plan for station {station}'
        with self.error_handling(msg):
            result = (self.session
                      .query(func.max(TrainStop.datehour_request))
                      .filter(TrainStop.station == station)
                      .scalar())

        return result

    def reset_db(self):
        self.drop_all()
        self.create_tables()
