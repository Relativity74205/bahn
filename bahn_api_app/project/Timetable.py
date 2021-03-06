from typing import Optional, List, Dict
from datetime import datetime
import logging

import config.config as config
from project.BahnAPI import BahnAPI
from project.TrainStopChange import TrainStopChange
from project.TrainStop import TrainStop


class Timetable:
    def __init__(self, bahn_api_object: BahnAPI):
        self.ba = bahn_api_object
        self.bahnhof_dict = config.bahnhof_dict

    def get_changes(self, station: str, request_type: str) -> List[TrainStopChange]:
        eva = self._get_eva(station)
        tstamp_request = datetime.now()
        request_type = request_type
        raw_tscs = self._get_raw_train_stop_changes(request_type, eva=eva)

        if raw_tscs is not None:
            if len(raw_tscs) == 0:
                train_stop_changes = []
            else:
                train_stop_changes = self._process_raw_tscs(raw_tscs, eva, station, request_type, tstamp_request)
        else:
            train_stop_changes = None

        return train_stop_changes

    def get_default_timetable(self, station: str, year: int, month: int, day: int, hour: int) -> List[TrainStop]:
        eva = self._get_eva(station)
        date = self._get_date(year, month, day)
        hour_filled = self._get_hour(hour)

        # TODO retry 2 times if fail, add try-except block
        raw_train_stops = self._get_raw_data('default', eva=eva, date=date, hour=hour_filled)

        if raw_train_stops is not None:
            if len(raw_train_stops) == 0:
                timetable = []
            else:
                timetable = self._process_raw_train_stops(raw_train_stops, eva, station, date, hour)
        else:
            timetable = None

        return timetable

    def get_timetable_json(self, station: str, year: int, month: int, day: int, hour: int) -> List[Dict]:
        timetable = self.get_default_timetable(station, year, month, day, hour)
        timetable_json = [train_stop.convert_to_dict() for train_stop in timetable]

        return timetable_json

    def _get_raw_train_stop_changes(self, request_type: str, eva: str) -> List:
        raw_train_stop_changes = self._get_raw_data(request_type, eva=eva)

        return raw_train_stop_changes

    def _get_raw_data(self, request_type: str, eva: str, date: str = None, hour: str = None) -> List:
        if eva is not None:
            if request_type == 'default':
                raw_dict = self.ba.get_default_plan(eva, date, hour)
            elif request_type == 'full':
                raw_dict = self.ba.get_full_changes(eva)
            elif request_type == 'recent':
                raw_dict = self.ba.get_recent_changes(eva)
            else:
                raw_dict = None
        else:
            raw_dict = None

        if raw_dict is not None:
            raw_data = self._get_train_stops(raw_dict)
        else:
            raw_data = None

        return raw_data

    @staticmethod
    def _process_raw_tscs(raw_tscs: List[Dict], eva: str, station: str, request_type: str,
                          tstamp_request: datetime) -> List[TrainStopChange]:
        # TODO
        if not isinstance(raw_tscs, list):
            raw_tscs = [raw_tscs]

        train_stop_changes = []
        for raw_tsc in raw_tscs:
            if isinstance(raw_tsc, dict):
                train_stop_change = TrainStopChange(raw_tsc, eva, station, request_type, tstamp_request)
                train_stop_changes.append(train_stop_change)
            else:
                logging.critical(f'raw train_stop_change ({raw_tsc}) is no dict, but of type {type(raw_tsc)}.')

        return train_stop_changes

    @staticmethod
    def _process_raw_train_stops(raw_train_stops: List[Dict], eva: str, station: str, date: str, hour: int) \
            -> List[TrainStop]:
        # TODO
        if not isinstance(raw_train_stops, list):
            raw_train_stops = [raw_train_stops]

        trainstops = []
        for raw_train_stop in raw_train_stops:
            ts = TrainStop()
            ts.create(raw_train_stop, eva, station, date, hour)
            if ts.planed_arrival_datetime is None or ts.planed_arrival_datetime.hour == hour:
                trainstops.append(ts)
        return trainstops

    @staticmethod
    def _get_train_stops(train_stop_dict: Dict) -> List:
        try:
            train_stops = train_stop_dict['timetable']
        except (KeyError, TypeError):
            train_stops = None

        if train_stops is not None:
            try:
                train_stops = train_stops['s']
            except (KeyError, TypeError):
                train_stops = []

        return train_stops

    @staticmethod
    def _get_station(default_plan_json: Dict) -> str:
        try:
            station = default_plan_json['timetable']['@station']
        except (KeyError, TypeError):
            station = None

        return station

    @staticmethod
    def _get_hour(hour: int) -> str:
        return str(hour).zfill(2)

    @staticmethod
    def _get_date(year: int, month: int, day: int) -> str:
        # TODO check for valid date
        return str(year)[-2:].zfill(2) + str(month).zfill(2) + str(day).zfill(2)

    def _get_eva(self, station: str) -> Optional[str]:
        try:
            eva = self.bahnhof_dict[station]['eva']
        except (KeyError, TypeError):
            eva = None

        return eva
