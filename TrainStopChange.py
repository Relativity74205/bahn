from datetime import datetime
from typing import Dict

from sqlalchemy import Column, Integer, String, DateTime

from Base import Base
import config.config as config


class TrainStopChange(Base):
    __tablename__ = 'trainstops_changes'

    change_id = Column(Integer, primary_key=True)
    tstamp_request = Column(DateTime)
    trainstop_id = Column(String)
    station = Column(String)
    eva_number = Column(String)
    arrival_cancellation_time = Column(DateTime)
    changed_arrival_datetime = Column(DateTime)
    changed_arrival_platform = Column(String)
    changed_arrival_from = Column(String)
    changed_arrival_status = Column(String)
    departure_cancellation_time = Column(DateTime)
    changed_departure_datetime = Column(DateTime)
    changed_departure_platform = Column(String)
    changed_departure_to = Column(String)
    changed_departure_status = Column(String)

    def __init__(self, raw_event_data: Dict, eva: str, station: str):
        self.raw_event = raw_event_data
        self.event_keys = raw_event_data.keys()
        self.trainstop_id = self._get_id()
        self.station = station
        self.eva_number = eva
        self.tstamp_request = datetime.now()

        self._set_arrival_paras()
        self._set_departure_paras()

    def _get_id(self):
        try:
            return self.raw_event[config.train_event_keys['id']]
        except KeyError:
            return None

    def _set_arrival_paras(self):
        if config.train_event_keys['arrival'] in self.event_keys:
            self.arrival_cancellation_time = self._get_cancellation_time('arrival_cancellation_time')
            changed_arrival_datetime = self._get_value('changed_arrival_datetime')
            self.changed_arrival_datetime = self._get_datetime(changed_arrival_datetime)
            self.changed_arrival_platform = self._get_value('changed_arrival_platform')
            self.changed_arrival_from = self._get_departure_place(self._get_value('changed_arrival_path'))
            self.changed_departure_status = self._get_value('changed_arrival_status')

    def _set_departure_paras(self):
        if config.train_event_keys['departure'] in self.event_keys:
            self.departure_cancellation_time = self._get_cancellation_time('departure_cancellation_time')
            changed_departure_datetime = self._get_value('changed_departure_datetime')
            self.changed_departure_datetime = self._get_datetime(changed_departure_datetime)
            self.changed_departure_platform = self._get_value('changed_departure_platform')
            self.changed_departure_to = self._get_destination_place(self._get_value('changed_departure_path'))
            self.changed_departure_status = self._get_value('changed_departure_status')

    def _get_cancellation_time(self, key: str) -> datetime:
        time_str = self._get_value(key)
        time = datetime.strptime(time_str, '%y%m%d%H:%M')

        return time

    def _get_value(self, key):
        try:
            keys = config.train_event_keys[key]
            value = self.raw_event[keys['para1']][keys['para2']]
        except KeyError:
            # TODO logging
            value = None

        return value

    @staticmethod
    def _get_departure_place(ppth: str):
        if ppth == '' or ppth is None:
            return None

        try:
            return ppth.split('|')[0]
        except IndexError:
            return None
        except AttributeError:
            return None

    @staticmethod
    def _get_destination_place(ppth: str):
        if ppth == '' or ppth is None:
            return None

        try:
            return ppth.split('|')[-1]
        except IndexError:
            return None
        except AttributeError:
            return None

    @staticmethod
    def _get_datetime(time_str):
        if time_str is not None:
            return datetime.strptime(time_str, '%y%m%d%H:%M')
        else:
            return None
