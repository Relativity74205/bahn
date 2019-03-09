from typing import Dict, Optional
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

import config.config as config
from DatabaseConnection import Base


class TrainStop(Base):
    __tablename__ = 'trainstops'

    trainstop_id = Column(String, primary_key=True)
    station = Column(String)
    eva_number = Column(Integer)
    trip_type = Column(String)
    filter_flags = Column(String)
    owner = Column(String)
    train_type = Column(String)
    train_number = Column(String)
    line = Column(String)
    planed_arrival_datetime = Column(DateTime)
    planed_arrival_platform = Column(String)
    planed_arrival_from = Column(String)
    planed_departure_datetime = Column(DateTime)
    planed_departure_platform = Column(String)
    planed_departure_to = Column(String)
    changed_arrival_datetime = Column(DateTime)
    changed_arrival_platform = Column(String)
    changed_arrival_from = Column(String)
    changed_departure_datetime = Column(DateTime)
    changed_departure_platform = Column(String)
    changed_departure_to = Column(String)
    message_ids_id = Column(Integer)

    def __init__(self, raw_event_data: Dict, station: str):
        self.raw_event = raw_event_data
        self.event_keys = raw_event_data.keys()
        self.trainstop_id = self._get_id()
        self.station = station
        # TODO
        self.eva_number = None
        self.trip_type = self._get_value('trip_type')
        self.filter_flags = self._get_value('filter_flags')
        self.owner = self._get_value('owner')
        self.train_type = self._get_value('train_type')
        self.train_number = self._get_value('train_number')
        self.line = self._get_line()
        self.planed_arrival_datetime = None
        self.planed_arrival_platform = None
        self.planed_arrival_from = None
        self.planed_departure_datetime = None
        self.planed_departure_platform = None
        self.planed_departure_to = None
        self.changed_arrival_datetime = None
        self.changed_arrival_platform = None
        self.changed_arrival_from = None
        self.changed_departure_datetime = None
        self.changed_departure_platform = None
        self.changed_departure_to = None
        self.message_id = None

        self._set_arrival_paras()
        self._set_departure_paras()

    def convert_to_dict(self):
        d = vars(self)
        try:
            d.pop('raw_event')
            d.pop('event_keys')
        except KeyError:
            pass

        return d

    def _get_id(self):
        try:
            return self.raw_event[config.train_event_keys['id']]
        except KeyError:
            return None

    def _set_arrival_paras(self):
        if config.train_event_keys['arrival'] in self.event_keys:
            arrival_datetime = self._get_value('arrival_datetime')
            self.planed_arrival_datetime = self._get_datetime(arrival_datetime)
            self.planed_arrival_platform = self._get_value('arrival_platform')
            self.planed_arrival_from = self._get_departure_place(self._get_value('arrival_path'))
        else:
            self.planed_arrival_datetime = None
            self.planed_arrival_platform = None
            self.planed_arrival_from = self.station

    def _set_departure_paras(self):
        if config.train_event_keys['departure'] in self.event_keys:
            departure_datetime = self._get_value('departure_datetime')
            self.planed_departure_datetime = self._get_datetime(departure_datetime)
            self.planed_departure_platform = self._get_value('departure_platform')
            self.planed_departure_to = self._get_destination_place(self._get_value('departure_path'))
        else:
            self.planed_departure_datetime = None
            self.planed_departure_platform = None
            self.planed_departure_to = self.station

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
    def _get_timestr(pt):
        if pt is not None and len(pt) == 10:
            return f'{pt[6:8]}:{pt[8:10]}:00'
        else:
            return None

    @staticmethod
    def _get_datestr(pt):
        if pt is not None and len(pt) >= 6:
            return f'20{pt[0:2]}-{pt[2:4]}-{pt[4:6]}'
        else:
            return None

    @staticmethod
    def _get_datetime(pt):
        date = TrainStop._get_datestr(pt)
        tstamp = TrainStop._get_timestr(pt)
        if tstamp is not None and date is not None:
            return datetime.strptime(f'{date} {tstamp}', '%Y-%m-%d %H:%M:%S')
        else:
            return None

    @staticmethod
    def _get_train_number(number, train_type):
        if number.isdigit():
            return train_type + number
        else:
            return number

    def _get_line(self):
        ar = config.train_event_keys['arrival']
        dp = config.train_event_keys['departure']
        line = config.train_event_keys['line']
        if ar in self.event_keys and line in self.raw_event[ar].keys():
            line = str(self._get_value('arrival_line'))
        elif dp in self.event_keys and line in self.raw_event[dp].keys():
            line = str(self._get_value('departure_line'))
        else:
            line = str(self.train_type) + str(self.train_number)

        if line.isdigit():
            return self.train_type + str(line)
        else:
            return line
