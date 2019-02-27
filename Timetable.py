from typing import Optional, List, Dict

import xmltodict

import config.config as config
from BahnAPI import BahnAPI
from TrainEvent import TrainEvent


class Timetable:
    def __init__(self, bahn_api_object: BahnAPI):
        self.ba = bahn_api_object
        self.bahnhof_dict = config.bahnhof_dict

    def get_timetable(self, station: str, year: int, month: int, day: int, hour: int):
        eva = self._get_eva(station)
        date = self._get_date(year, month, day)
        hour = self._get_hour(hour)

        if eva is not None:
            default_plan = self.ba.get_default_plan(eva, date, hour)
        else:
            default_plan = None

        if default_plan is not None:
            default_plan_json = self._get_default_plan_json(default_plan)
        else:
            default_plan_json = None

        if default_plan_json is not None:
            raw_train_events = self._get_train_events(default_plan_json)
        else:
            raw_train_events = None

        if raw_train_events is not None:
            timetable = self._process_raw_train_events(raw_train_events, station)
        else:
            timetable = None

        return timetable

    def get_timetable_json(self, station: str, year: int, month: int, day: int, hour: int) -> List[Dict]:
        timetable = self.get_timetable(station, year, month, day, hour)
        timetable_json = [event.convert_to_dict() for event in timetable]

        return timetable_json

    @staticmethod
    def _process_raw_train_events(raw_train_events: List[Dict], station: str) -> List[TrainEvent]:
        return [TrainEvent(train_event, station) for train_event in raw_train_events]

    @staticmethod
    def _get_default_plan_json(default_plan: str) -> Dict:
        default_plan_json = xmltodict.parse(default_plan)

        return default_plan_json

    @staticmethod
    def _get_train_events(default_plan_json: Dict) -> List:
        try:
            train_events = default_plan_json['timetable']['s']
        except KeyError:
            train_events = None

        return train_events

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
