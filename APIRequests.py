import time
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

import DatabaseConnection
import BahnAPI
import Timetable
import config.config as config
import timetable_date_functions as tdf
from TrainStopChange import TrainStopChange
from RequestsHeap import RequestsHeap


class APIRequests:
    def __init__(self):
        self.requests_heap = RequestsHeap()

        self.db = DatabaseConnection.DatabaseConnection()
        self.ba = BahnAPI.BahnAPI()
        self.timetable = Timetable.Timetable(self.ba)
        self.stations = config.stations

        self.recent_request_lifetime = config.RECENT_REQUEST_LIFETIME
        self.hours_between_updates = config.HOURS_BETWEEN_UPDATES
        self.last_complete_update: Dict[str, Optional[datetime]] = {'default': None,
                                                                    'full': None}
        self.last_single_update = self._init_last_update()
        self.sleep_time_between_loops = config.SLEEP_TIME_BETWEEN_UPDATES
        self.max_default_plans = config.MAX_DEFAULT_PLANS
        self.min_seconds_between_requests = config.MIN_SECONDS_BETWEEN_REQUESTS

    def _init_last_update(self) -> Dict[str, Any]:
        last_single_update = {}
        for station in self.stations:
            last_single_update[station] = {'default': None,
                                           'full': None,
                                           'recent': None}

        return last_single_update

    def main_loop(self):
        while True:
            try:
                if self.load_next(update_type='default'):
                    self.get_default_tables()
                if self.load_next(update_type='full'):
                    self.get_update(full_update=True)
                self.get_update()
            except Exception as e:
                logging.critical(f'Unknown Error; error_msg: {str(e)}')
            self.sleep(sleep_type='loop', sleep_time=self.sleep_time_between_loops)

    def wait_for_available_requests(self, requests_needed, func_name, station):
        logging.debug(f'Starting to get {func_name} for station: {station}; checking if waiting is necessary')
        while True:
            if self.requests_heap.get_available_requests() < requests_needed:
                waittime = self.requests_heap.get_age_oldest_request()
                logging.debug(f'Waiting for {waittime} seconds')
                time.sleep(waittime)
            else:
                logging.debug(f'no (more) waiting necessary; returning to calling function/method')
                return

    def load_next(self, update_type: str) -> True:
        logging.debug(f'Checking if {update_type} data should be loaded')
        current_time: datetime = datetime.now()
        tstamp_last_update: datetime = self.last_complete_update[update_type]
        logging.debug(f'load_next_updates (update_type {update_type}); '
                      f'details: current_time {current_time}, '
                      f'tstamp_last_update {tstamp_last_update}, '
                      f'hours_between_updates {self.hours_between_updates[update_type]}')
        if tstamp_last_update is None:
            logging.debug(f'load_next_updates (update_type {update_type}): True')
            return True
        elif (current_time - tstamp_last_update).total_seconds()/(60*60) >= self.hours_between_updates[update_type]:
            logging.debug(f'load_next_updates (update_type {update_type}): True')
            return True
        else:
            logging.debug(f'load_next_updates (update_type {update_type}): False')
            return False

    def get_default_tables(self):
        logging.debug('Starting getting default tables')
        current_time = datetime.now()

        train_stops = []
        for station in self.stations:
            # TODO refactor own function
            last_datehour = self.db.get_last_datehour_default_plan(station)
            missing_datehours = tdf.get_missing_default_plan_dates(current_time, last_datehour, self.max_default_plans)
            logging.debug(f'last_datehour: {last_datehour}; missing_datehours: {missing_datehours}')

            for datehour in missing_datehours:
                self.wait_for_available_requests(requests_needed=1, func_name='default_tables', station=station)

                new_train_stops = self.timetable.get_default_timetable(station, *datehour)
                if new_train_stops is not None:
                    train_stops += new_train_stops
                    logging.debug(f'Got successfully {len(new_train_stops)} default table(s) '
                                  f'for station {station} and datehour {datehour}')
                else:
                    logging.critical(f'get_default_tables: new_timetables for station {station} is None!')
                self.requests_heap.append_event()

        self.last_complete_update['default'] = datetime.now()
        logging.debug('Ended getting default plans, commiting to database')
        self.save_data(train_stops, 'TrainStop')

    def get_update(self, full_update: bool = False):
        train_stop_changes = []
        logging.debug(f'Starting getting update; full_update: {full_update}')
        for station in config.stations:
            self.wait_for_available_requests(requests_needed=1,
                                             func_name=f'update; full_update: {full_update}', station=station)

            if full_update:
                new_train_stop_changes = self.get_single_update(station, request_type='full')
            else:
                short_time_since_last_update, sleep_time = self.short_time_since_last_update(station)
                self.sleep(sleep_type='short_time_since_last_update', sleep_time=sleep_time)
                if short_time_since_last_update:
                    new_train_stop_changes = self.get_single_update(station, request_type='recent')
                else:
                    new_train_stop_changes = self.get_single_update(station, request_type='full')

            if new_train_stop_changes is not None:
                train_stop_changes += new_train_stop_changes
                logging.info(f'Got {len(new_train_stop_changes)} update(s) for station: {station}; '
                             f'full_update: {full_update}')
            else:
                logging.critical(f'get_single_updates: new_train_stop_changes for station {station} is None;'
                                 f'full_update: {full_update}')

            self.requests_heap.append_event()

        if full_update:
            self.last_complete_update['full'] = datetime.now()
            logging.debug(f'Set last_complete_full_update to {self.last_complete_update["full"]}.')

        logging.debug('Ended getting regular updates, starting to commit to database')
        self.save_data(train_stop_changes, 'TrainStopChange')

    def get_single_update(self, station: str, request_type: str) -> List[TrainStopChange]:
        logging.debug(f'Getting update for {station}; request_type: {request_type}')
        train_stop_changes = self.timetable.get_changes(station=station, request_type=request_type)

        self.last_single_update[station]['recent'] = datetime.now()
        if request_type == 'full':
            self.last_single_update[station]['full'] = datetime.now()
        logging.debug(f'Got update for {station} finished; request_type: {request_type}')

        return train_stop_changes

    def short_time_since_last_update(self, station: str) -> (bool, float):
        # TODO refactor
        current_time = datetime.now()
        if self.last_single_update[station]['recent'] is not None:
            last_time = self.last_single_update[station]['recent']
        elif self.last_single_update[station]['full'] is not None:
            last_time = self.last_single_update[station]['full']
        else:
            last_time = self.db.get_last_tstamp_request(station=station)
        logging.debug(f'short_time_since_last_update; current_time: {current_time}, last_time: {last_time}')

        if last_time is not None:
            delta = (current_time - last_time).total_seconds()
            short_time_since_last_update = delta < self.recent_request_lifetime
            logging.debug(f'short_time_since_last_update: {short_time_since_last_update}; delta: {delta}')
            return short_time_since_last_update, self.min_seconds_between_requests - delta
        else:
            logging.debug(f'short_time_since_last_update: False')
            return False, -1

    @staticmethod
    def sleep(sleep_type: str, sleep_time: float):
        if sleep_type == 'loop':
            logging.debug(f'Sleep for {sleep_time} seconds.')
            time.sleep(sleep_time)
        else:
            if sleep_time > 0:
                logging.debug(f'Too early for next recent update, sleeping for {sleep_time}')
                time.sleep(sleep_time)

    def save_data(self, objects, obj_name):
        # TODO add save to file if db throws exception
        if objects is not None and len(objects) > 0:
            self.db.save_bulk(objects, obj_name)
            logging.debug(f'Ended to commit {obj_name} to database')
        else:
            logging.critical('Nothing to commit to database')
