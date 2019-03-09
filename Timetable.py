from typing import Optional, List, Dict

import xmltodict

import config.config as config
from BahnAPI import BahnAPI
from TrainStop import TrainStop


class Timetable:
    def __init__(self, bahn_api_object: BahnAPI):
        self.ba = bahn_api_object
        self.bahnhof_dict = config.bahnhof_dict

    def update_timetable(self, station: str):
        raw_train_stop_changes = self._get_raw_train_stop_changes(station)

        if raw_train_stop_changes is not None:
            # TODO
            train_stop = self._process_raw_train_stop_changes(raw_train_stop_changes, station)

    def save_default_timetable(self, station: str, year: int, month: int, day: int, hour: int):
        # TODO
        timetable = self.get_default_timetable(station, year, month, day, hour)

    def get_default_timetable(self, station: str, year: int, month: int, day: int, hour: int) -> List[TrainStop]:
        eva = self._get_eva(station)
        date = self._get_date(year, month, day)
        hour = self._get_hour(hour)

        raw_train_stops = self._get_raw_data(eva=eva, date=date, hour=hour)

        if raw_train_stops is not None:
            timetable = self._process_raw_train_stops(raw_train_stops, station)
        else:
            timetable = None

        return timetable

    def get_timetable_json(self, station: str, year: int, month: int, day: int, hour: int) -> List[Dict]:
        timetable = self.get_default_timetable(station, year, month, day, hour)
        timetable_json = [train_stop.convert_to_dict() for train_stop in timetable]

        return timetable_json

    def _get_raw_train_stop_changes(self, station: str) -> List:
        eva = self._get_eva(station)

        raw_train_stop_changes = self._get_raw_data(eva=eva)

        return raw_train_stop_changes

    def _get_raw_data(self, eva, date=None, hour=None) -> List:
        if eva is not None:
            if date is not None:
                raw_str = self.ba.get_default_plan(eva, date, hour)
            else:
                raw_str = self.ba.get_recent_changes(eva)
        else:
            raw_str = None

        if raw_str is not None:
            raw_dict = self._xml_to_json(raw_str)
        else:
            raw_dict = None

        if raw_dict is not None:
            raw_data = self._get_train_stops(raw_dict)
        else:
            raw_data = None

        return raw_data

    def _process_raw_train_stop_changes(self, raw_train_stop_changes: List[Dict], station: str) -> List[TrainStop]:
        return [self._process_raw_train_stop_change_single(train_stop_change, station)
                    for train_stop_change in raw_train_stop_changes]

    @staticmethod
    def _process_raw_train_stop_change_single(train_stop_change: Dict, station: str) -> TrainStop:
        train_stop = get_train_stop_from_db(train_stop_change)
        if train_stop is None:
            train_stop = TrainStop(train_stop_change, station)

        return train_stop

    @staticmethod
    def _process_raw_train_stops(raw_train_stops: List[Dict], station: str) -> List[TrainStop]:
        return [TrainStop(raw_train_stop, station) for raw_train_stop in raw_train_stops]

    @staticmethod
    def _xml_to_json(xml_str: str) -> Dict:
        # TODO error handling
        json_dict = xmltodict.parse(xml_str)

        return json_dict

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
