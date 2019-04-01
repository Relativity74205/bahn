from typing import Optional, List, Dict
from datetime import datetime
import logging

from sqlalchemy.exc import SQLAlchemyError

import config.config as config
from BahnAPI import BahnAPI
from TrainStopChange import TrainStopChange
from TrainStop import TrainStop
from DatabaseConnection import DatabaseConnection


class Timetable:
    def __init__(self, bahn_api_object: BahnAPI, db: DatabaseConnection):
        self.ba = bahn_api_object
        self.bahnhof_dict = config.bahnhof_dict
        self.db = db

    def get_changes(self, station: str, request_type: str) -> List[TrainStopChange]:
        eva = self._get_eva(station)
        tstamp_request = datetime.now()
        request_type = request_type
        raw_tscs = self._get_raw_train_stop_changes(request_type, eva=eva)

        if raw_tscs is not None:
            train_stop_changes = self._process_raw_tscs(raw_tscs, eva, station, request_type, tstamp_request)
        else:
            train_stop_changes = None

        try:
            self.db.save_bulk(train_stop_changes, 'TrainStopChanges')
        except SQLAlchemyError as e:
            logging.critical(f'Error while writing TrainStops into DB; error_msg: {str(e)}')
            if 'constraint failed' in str(e):
                logging.critical('At least one dataset already in DB, switching to fallback')
                # TODO create fallback function (instead of bulk insert, insert single line and looking before)

        return train_stop_changes

    def get_default_timetable(self, station: str, year: int, month: int, day: int, hour: int) -> List[TrainStop]:
        eva = self._get_eva(station)
        date = self._get_date(year, month, day)
        hour_filled = self._get_hour(hour)

        # TODO retry 2 times if fail, add try-except block
        raw_train_stops = self._get_raw_data('default', eva=eva, date=date, hour=hour_filled)

        if raw_train_stops is not None:
            timetable = self._process_raw_train_stops(raw_train_stops, eva, station, date, hour)
        else:
            timetable = None

        # TODO refactor
        if timetable is not None:
            try:
                self.db.save_bulk(timetable, 'TrainStops')
            except SQLAlchemyError as e:
                logging.critical(f'Error while writing TrainStops into DB; error_msg: {str(e)}')
                if 'constraint failed' in str(e):
                    logging.critical('At least one dataset already in DB, switching to fallback')
                    # TODO create fallback function (instead of bulk insert, insert single line and looking before)

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

    def _process_raw_tscs(self, raw_tscs: List[Dict], eva: str, station: str, request_type: str,
                          tstamp_request: datetime) -> List[TrainStopChange]:
        return [self._process_raw_tsc_single(train_stop_change, eva, station, request_type, tstamp_request)
                for train_stop_change in raw_tscs]

    def _process_raw_tsc_single(self, raw_tsc: Dict, eva: str, station: str, request_type: str,
                                tstamp_request: datetime) -> TrainStopChange:
        train_stop_change = TrainStopChange(raw_tsc, eva, station, request_type, tstamp_request)

        # TODO refactor, remove db from Timetable
        if train_stop_change.trainstop_id is not None:
            train_stop: TrainStop = self.db.get_by_pk(TrainStop, train_stop_change.trainstop_id)
        else:
            train_stop = None

        if train_stop is not None:
            train_stop.update(train_stop_change)
            self.db.session.add(train_stop)

        return train_stop_change

    @staticmethod
    def _process_raw_train_stops(raw_train_stops: List[Dict], eva: str, station: str, date: str, hour: int) \
            -> List[TrainStop]:
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
            train_stops = train_stop_dict['timetable']['s']
        except KeyError:
            train_stops = None

        return train_stops

    @staticmethod
    def _get_station(default_plan_json: Dict) -> str:
        try:
            station = default_plan_json['timetable']['@station']
        except KeyError:
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
        except KeyError:
            eva = None

        return eva
