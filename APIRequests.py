from datetime import datetime

import DatabaseConnection
import BahnAPI
import Timetable
import config.config as config
import timetable_date_functions as tdf
from TrainStop import TrainStop
from TrainStopChange import TrainStopChange
from RequestsHeap import RequestsHeap


class APIRequests:
    def __init__(self):
        self.requests_heap = RequestsHeap()

        self.db = DatabaseConnection.DatabaseConnection()
        self.ba = BahnAPI.BahnAPI()
        self.timetable = Timetable.Timetable(self.ba)

        # TODO move to config
        self.recent_request_lifetime = 115

    def main_loop(self):
        while True:
            self.check_default_tables()
            self.check_updates()

    def check_default_tables(self):
        current_time = datetime.now()
        for station in config.stations:
            last_datehour = self.db.get_last_datehour_default_plan(station)
            missing_datehours = tdf.get_missing_default_plan_dates(current_time, last_datehour)
            for datehour in missing_datehours:
                if self.requests_heap.check_requests_heap():
                    self.requests_heap.append_event()
                    timetable = self.timetable.get_default_timetable(station, *datehour)
                    self.db.save_bulk(timetable, 'TrainStop')

    def check_updates(self):
        train_stop_changes = []
        for station in config.stations:
            if self.short_time_since_last_update(station):
                train_stop_changes = self.timetable.get_changes(station=station, request_type='recent')
            else:
                train_stop_changes = self.timetable.get_changes(station=station, request_type='full')

        [self.process_train_stop_changes(train_stop_change) for train_stop_change in train_stop_changes]
        self.db.session.commit()

        self.db.save_bulk(train_stop_changes, 'TrainStopChange')

    def process_train_stop_changes(self, train_stop_change: TrainStopChange):
        if train_stop_change.trainstop_id is not None:
            train_stop: TrainStop = self.db.get_by_pk(TrainStop, train_stop_change.trainstop_id)
        else:
            train_stop = None

        if train_stop is not None:
            train_stop.update(train_stop_change)
            self.db.session.add(train_stop)

    def short_time_since_last_update(self, station: str) -> bool:
        current_time = datetime.now()
        last_time = self.db.get_last_tstamp_request(station=station)
        delta = (current_time - last_time).total_seconds()

        return delta < self.recent_request_lifetime
