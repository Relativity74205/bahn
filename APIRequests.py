import time
import logging
from typing import List, Dict, Any, Optional
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
        self.stations = config.stations

        self.recent_request_lifetime = config.RECENT_REQUEST_LIFETIME
        self.hours_between_updates = config.HOURS_BETWEEN_UPDATES
        self.last_complete_update: Dict[str, Optional[datetime]] = {'default': None,
                                                                    'full': None}
        self.last_single_update = self._init_last_update()
        self.sleep_time = config.SLEEP_TIME_BETWEEN_UPDATES
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
                logging.debug('Checking if default tables should be loaded')
                if self.load_next_updates(update_type='default'):
                    logging.info('Getting default table updates')
                    self.get_default_tables()

                logging.debug('Checking if full update should be loaded')
                if self.load_next_updates(update_type='full'):
                    logging.info('Getting full update')
                    self.get_full_update()

                logging.debug('Getting updates')
                self.get_single_updates()

                logging.debug(f'Sleep for {self.sleep_time} seconds.')
            except Exception as e:
                logging.critical(f'Unknown Error; error_msg: {str(e)}')
            time.sleep(self.sleep_time)

    def wait_for_available_requests(self, requests_needed: int = 1):
        while True:
            if self.requests_heap.get_available_requests() < requests_needed:
                waittime = self.requests_heap.get_age_oldest_request()
                logging.debug(f'Waiting for {waittime} seconds')
                time.sleep(waittime)
            else:
                logging.debug(f'no (more) waiting necessary; returning to calling function/method')
                return

    def load_next_updates(self, update_type: str) -> True:
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
        current_time = datetime.now()

        timetables = []
        for station in self.stations:
            logging.debug(f'Starting to get default tables for station: {station}; waiting for available requests')
            self.wait_for_available_requests(requests_needed=1)

            last_datehour = self.db.get_last_datehour_default_plan(station)
            missing_datehours = tdf.get_missing_default_plan_dates(current_time, last_datehour, self.max_default_plans)
            logging.debug(f'last_datehour: {last_datehour}; missing_datehours: {missing_datehours}')
            for datehour in missing_datehours:
                logging.debug(f'Getting default tables for station {station} and datehour {datehour}')
                self.requests_heap.append_event()
                new_timetables = self.timetable.get_default_timetable(station, *datehour)
                if new_timetables is not None:
                    timetables += new_timetables
        self.last_complete_update['default'] = datetime.now()
        logging.debug('Ended getting default plans, commiting to database')

        self.db.save_bulk(timetables, 'TrainStop')
        logging.debug('Commited default plans to database')

    def get_full_update(self):
        train_stop_changes = []
        for station in config.stations:
            logging.debug(f'Starting to get full update for station: {station}; waiting for available requests')
            self.wait_for_available_requests(requests_needed=1)

            train_stop_changes += self.timetable.get_changes(station=station, request_type='full')
            self.last_single_update[station]['full'] = datetime.now()
            self.requests_heap.append_event()
            logging.debug(f'Got full update for station: {station}')
        self.last_complete_update['full'] = datetime.now()

        logging.debug('Ended getting full updates, processing updates')
        [self.update_train_stops_with_changes(train_stop_change) for train_stop_change in train_stop_changes]
        logging.debug('Ended processing updates, starting to commit to database')
        self.db.session.commit()
        self.db.save_bulk(train_stop_changes, 'TrainStopChange')
        logging.debug('Ended to commit to database')

    def get_single_updates(self):
        train_stop_changes = []
        logging.debug('Starting getting regular updates')
        for station in config.stations:
            logging.info(f'Starting to get update for {station}; waiting for available requests')
            self.wait_for_available_requests(requests_needed=1)

            sleep_time = self.short_time_since_last_update(station)
            if sleep_time:
                logging.debug(f'Too early for next recent update, sleeping for {sleep_time}')
                time.sleep(sleep_time)
                new_train_stop_changes = self.get_single_update(station, request_type='recent')
            else:
                new_train_stop_changes = self.get_single_update(station, request_type='full')
            if new_train_stop_changes is not None:
                train_stop_changes += new_train_stop_changes

            self.requests_heap.append_event()
            logging.info(f'Got update for station: {station}')

        logging.debug('Ended getting regular updates, processing updates')
        [self.update_train_stops_with_changes(train_stop_change) for train_stop_change in train_stop_changes]
        logging.debug('Ended processing updates, starting to commit to database')
        self.db.session.commit()
        self.db.save_bulk(train_stop_changes, 'TrainStopChange')
        logging.debug('Ended to commit to database')

    def get_single_update(self, station: str, request_type: str) -> List[TrainStopChange]:
        logging.debug(f'Getting update for {station}; request_type: {request_type}')
        train_stop_changes = self.timetable.get_changes(station=station, request_type=request_type)
        self.last_single_update[station][request_type] = datetime.now()
        logging.debug(f'Got update for {station} finished; request_type: {request_type}')

        return train_stop_changes

    def update_train_stops_with_changes(self, train_stop_change: TrainStopChange):
        if train_stop_change.trainstop_id is not None:
            # logging.debug(f'Getting TrainStop for trainstop_id {train_stop_change.trainstop_id}')
            train_stop: TrainStop = self.db.get_by_pk(TrainStop, train_stop_change.trainstop_id)
        else:
            train_stop = None

        if train_stop is not None:
            # logging.debug('TrainStop found, updating...')
            train_stop.update(train_stop_change)
            self.db.session.add(train_stop)
            # logging.debug('TrainStop update finished and commited to database')

    def short_time_since_last_update(self, station: str) -> Optional[float]:
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
            return self.min_seconds_between_requests - delta
        else:
            logging.debug(f'short_time_since_last_update: False')
            return None
