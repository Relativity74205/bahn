from typing import Dict
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

import config.config as config
from Base import Base
from TrainStopChange import TrainStopChange


class TrainStop(Base, TrainStopChange):
    __tablename__ = 'trainstops'

    trainstop_id = Column(String, primary_key=True)
    station = Column(String)
    eva_number = Column(String)
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
    departure_delay = Column(Integer)
    arrival_delay = Column(Integer)
    flag_cancelled_arrival = Column(Integer)
    flag_cancelled_departure = Column(Integer)
    flag_delayed_departure = Column(Integer)
    flag_delayed_arrival = Column(Integer)
    flag_changed_platform = Column(Integer)

    def __init__(self):
        self.raw_event = None
        self.event_keys = None

    def create(self, raw_event_data: Dict, eva: str, station: str):
        self.raw_event = raw_event_data
        self.event_keys = raw_event_data.keys()
        self.trainstop_id = self._get_id()
        self.station = station
        self.eva_number = eva
        self.trip_type = self._get_value('trip_type')
        self.filter_flags = self._get_value('filter_flags')
        self.owner = self._get_value('owner')
        self.train_type = self._get_value('train_type')
        self.train_number = self._get_value('train_number')
        self.line = self._get_line()
        self._set_arrival_paras()
        self._set_departure_paras()

    def update(self, train_stop: TrainStopChange):
        self.arrival_cancellation_time = train_stop.arrival_cancellation_time
        self.changed_arrival_datetime = train_stop.changed_arrival_datetime
        self.changed_arrival_platform = train_stop.changed_arrival_platform
        self.changed_arrival_from = train_stop.changed_arrival_from
        self.changed_arrival_status = train_stop.changed_arrival_status
        self.departure_cancellation_time = train_stop.departure_cancellation_time
        self.changed_departure_datetime = train_stop.changed_departure_datetime
        self.changed_departure_platform = train_stop.changed_departure_platform
        self.changed_departure_to = train_stop.changed_departure_to
        self.changed_departure_status = train_stop.changed_departure_status
        self.departure_delay = self._calc_delay(self.changed_departure_datetime, self.planed_departure_datetime)
        self.arrival_delay = self._calc_delay(self.changed_arrival_datetime, self.planed_arrival_datetime)
        self.flag_cancelled_arrival = self._calc_flag_cancelled(self.changed_arrival_status)
        self.flag_cancelled_departure = self._calc_flag_cancelled(self.changed_departure_status)
        self.flag_delayed_departure = self._calc_flag_delayed(self.changed_departure_datetime)
        self.flag_delayed_arrival = self._calc_flag_delayed(self.changed_arrival_datetime)
        self.flag_changed_platform = self._calc_changed_platform(self.changed_departure_platform,
                                                                 self.changed_arrival_platform)

    def convert_to_dict(self):
        d = vars(self)
        try:
            d.pop('raw_event')
            d.pop('event_keys')
            d.pop('_sa_instance_state')
        except KeyError:
            pass

        return d

    @staticmethod
    def _calc_flag_cancelled(changed_status):
        if changed_status == 'c':
            return 1
        else:
            return 0

    @staticmethod
    def _calc_changed_platform(changed_departure_platform, changed_arrival_platform):
        if changed_arrival_platform is None and changed_departure_platform is None:
            return 0
        else:
            return 1

    @staticmethod
    def _calc_flag_delayed(changed_time):
        if changed_time is None:
            return 0
        else:
            return 1

    @staticmethod
    def _calc_delay(planned_time: datetime, changed_time: datetime) -> int:
        if changed_time is None:
            return 0
        else:
            (changed_time - planned_time).total_seconds()

    def _set_arrival_paras(self):
        if config.train_event_keys['arrival'] in self.event_keys:
            arrival_datetime = self._get_value('arrival_datetime')
            self.planed_arrival_datetime = self._get_datetime(arrival_datetime)
            self.planed_arrival_platform = self._get_value('arrival_platform')
            self.planed_arrival_from = self._get_departure_place(self._get_value('arrival_path'))

    def _set_departure_paras(self):
        if config.train_event_keys['departure'] in self.event_keys:
            departure_datetime = self._get_value('departure_datetime')
            self.planed_departure_datetime = self._get_datetime(departure_datetime)
            self.planed_departure_platform = self._get_value('departure_platform')
            self.planed_departure_to = self._get_destination_place(self._get_value('departure_path'))

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
