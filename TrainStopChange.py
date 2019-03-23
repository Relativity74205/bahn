from datetime import datetime
from typing import Dict, Optional

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from TrainStop import TrainStop
from Base import Base
import config.config as config


class TrainStopChange(Base):
    __tablename__ = 'trainstops_changes'

    change_id = Column(Integer, primary_key=True)
    station = Column(String)
    eva_number = Column(String)
    request_type = Column(String)
    tstamp_request = Column(DateTime)
    trainstop_id = Column(String, ForeignKey('trainstops.trainstop_id'))
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

    def __init__(self, raw_event_data: Dict, eva: str, station: str, request_type: str, tstamp_request: datetime):
        self.raw_event = raw_event_data
        self.event_keys = raw_event_data.keys()
        self.trainstop_id = TrainStop.get_id(self.raw_event)
        self.station = station
        self.eva_number = eva
        self.request_type = request_type
        self.tstamp_request = tstamp_request

        self._set_arrival_paras()
        self._set_departure_paras()

    def _set_arrival_paras(self):
        if config.train_event_keys['arrival'] in self.event_keys:
            self.arrival_cancellation_time = self._get_cancellation_time('arrival_cancellation_time')
            changed_arrival_datetime = TrainStop.get_value(self.raw_event, 'changed_arrival_datetime')
            self.changed_arrival_datetime = TrainStop.get_datetime(changed_arrival_datetime)
            self.changed_arrival_platform = TrainStop.get_value(self.raw_event, 'changed_arrival_platform')
            self.changed_arrival_from = TrainStop.get_departure_place(TrainStop.get_value(self.raw_event,
                                                                                          'changed_arrival_path'))
            self.changed_arrival_status_status = TrainStop.get_value(self.raw_event, 'changed_arrival_status')

    def _set_departure_paras(self):
        if config.train_event_keys['departure'] in self.event_keys:
            self.departure_cancellation_time = self._get_cancellation_time('departure_cancellation_time')
            changed_departure_datetime = TrainStop.get_value(self.raw_event, 'changed_departure_datetime')
            self.changed_departure_datetime = TrainStop.get_datetime(changed_departure_datetime)
            self.changed_departure_platform = TrainStop.get_value(self.raw_event, 'changed_departure_platform')
            self.changed_departure_to = TrainStop.get_destination_place(TrainStop.get_value(self.raw_event,
                                                                                            'changed_departure_path'))
            self.changed_departure_status = TrainStop.get_value(self.raw_event, 'changed_departure_status')

    def _get_cancellation_time(self, key: str) -> Optional[datetime]:
        time_str = TrainStop.get_value(self.raw_event, key)
        if time_str is None:
            return None

        try:
            return datetime.strptime(time_str, '%y%m%d%H%M')
        except ValueError:
            # TODO logging
            return None
