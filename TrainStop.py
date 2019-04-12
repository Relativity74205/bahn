from typing import Dict, Optional
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

import config.config as config
from Base import Base


class TrainStop(Base):
    __tablename__ = 'trainstops'

    trainstop_id = Column(String, primary_key=True)
    datehour_request = Column(String)
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

    def create(self, raw_event_data: Dict, eva: str, station: str, date: str, hour: int):
        self.raw_event = raw_event_data
        self.event_keys = raw_event_data.keys()
        self.datehour_request = self._get_datehour_request(date, hour)
        self.trainstop_id = self.get_id(self.raw_event)
        self.station = station
        self.eva_number = eva
        self.trip_type = self.get_value(self.raw_event, 'trip_type')
        self.filter_flags = self.get_value(self.raw_event, 'filter_flags')
        self.owner = self.get_value(self.raw_event, 'owner')
        self.train_type = self.get_value(self.raw_event, 'train_type')
        self.train_number = self.get_value(self.raw_event, 'train_number')
        self.line = self._get_line()
        self._set_arrival_paras()
        self._set_departure_paras()

    def update(self, train_stop_change):
        self.departure_delay = self._calc_delay(train_stop_change.changed_departure_datetime,
                                                self.planed_departure_datetime)
        self.arrival_delay = self._calc_delay(train_stop_change.changed_arrival_datetime,
                                              self.planed_arrival_datetime)
        self.flag_cancelled_arrival = self._calc_flag_cancelled(train_stop_change.changed_arrival_status)
        self.flag_cancelled_departure = self._calc_flag_cancelled(train_stop_change.changed_departure_status)
        self.flag_delayed_departure = self._calc_flag_delayed(train_stop_change.changed_departure_datetime)
        self.flag_delayed_arrival = self._calc_flag_delayed(train_stop_change.changed_arrival_datetime)
        self.flag_changed_platform = self._calc_changed_platform(train_stop_change.changed_departure_platform,
                                                                 train_stop_change.changed_arrival_platform)

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
        if changed_time is None or planned_time is None:
            return 0
        else:
            (changed_time - planned_time).total_seconds()

    def _set_arrival_paras(self):
        if config.train_event_keys['arrival'] in self.event_keys:
            arrival_datetime = self.get_value(self.raw_event, 'arrival_datetime')
            self.planed_arrival_datetime = self.get_datetime(arrival_datetime)
            self.planed_arrival_platform = self.get_value(self.raw_event, 'arrival_platform')
            self.planed_arrival_from = self.get_departure_place(self.get_value(self.raw_event, 'arrival_path'))

    def _set_departure_paras(self):
        if config.train_event_keys['departure'] in self.event_keys:
            departure_datetime = self.get_value(self.raw_event, 'departure_datetime')
            self.planed_departure_datetime = self.get_datetime(departure_datetime)
            self.planed_departure_platform = self.get_value(self.raw_event, 'departure_platform')
            self.planed_departure_to = self.get_destination_place(self.get_value(self.raw_event, 'departure_path'))

    @staticmethod
    def _get_train_number(number, train_type):
        if number.isdigit():
            return train_type + number
        else:
            return number

    def _get_line(self) -> Optional[str]:
        ar = config.train_event_keys['arrival']
        dp = config.train_event_keys['departure']
        line = config.train_event_keys['line']
        if ar in self.event_keys and line in self.raw_event[ar].keys():
            line = str(self.get_value(self.raw_event, 'arrival_line'))
        elif dp in self.event_keys and line in self.raw_event[dp].keys():
            line = str(self.get_value(self.raw_event, 'departure_line'))
        else:
            line = str(self.train_type) + str(self.train_number)

        if line.isdigit():
            return self.train_type + str(line)
        else:
            return line

    @staticmethod
    def get_value(raw_event: Dict, key: str) -> Optional[str]:
        try:
            keys = config.train_event_keys[key]
            value = raw_event[keys['para1']][keys['para2']]
        except (KeyError, TypeError):
            # TODO logging
            value = None

        return value

    @staticmethod
    def get_id(raw_event: Dict) -> Optional[str]:
        try:
            return raw_event[config.train_event_keys['id']]
        except (KeyError, TypeError):
            return None

    @staticmethod
    def get_datetime(time_str: str) -> Optional[datetime]:
        if time_str is None:
            return None

        try:
            return datetime.strptime(time_str, '%y%m%d%H%M')
        except ValueError as e:
            # TODO logging
            return None

    @staticmethod
    def get_departure_place(ppth: str) -> Optional[str]:
        if ppth == '' or ppth is None:
            return None

        try:
            return ppth.split('|')[0]
        except IndexError:
            return None
        except AttributeError:
            return None

    @staticmethod
    def get_destination_place(ppth: str) -> Optional[str]:
        if ppth == '' or ppth is None:
            return None

        try:
            return ppth.split('|')[-1]
        except IndexError:
            return None
        except AttributeError:
            return None

    @staticmethod
    def _get_datehour_request(date: str, hour: int) -> str:
        return date + str(hour).zfill(2)
