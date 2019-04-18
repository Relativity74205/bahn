import time
import logging
from typing import List

import DatabaseConnection
import BahnAPI
import Timetable
from TrainStop import TrainStop
from TrainStopChange import TrainStopChange


def main():
    set_logging_config()
    db = DatabaseConnection.DatabaseConnection()
    db.reset_db()

    ba = BahnAPI.BahnAPI()

    timetable = Timetable.Timetable(ba)
    get_default_time_table(db, timetable, 'Recklinghausen Hbf', 2019, 4, 18, 21)
    get_changes(db, timetable, 'Recklinghausen Hbf', 'recent')
    # get_changes(timetable, 'Duisburg Hbf', 'recent'))
    # get_bahnhof_dict(ba)

def update_train_stops_with_changes(db, train_stop_change: TrainStopChange):
    if train_stop_change.trainstop_id is not None:
        # logging.debug(f'Getting TrainStop for trainstop_id {train_stop_change.trainstop_id}')
        train_stop: TrainStop = db.get_by_pk(TrainStop, train_stop_change.trainstop_id)
    else:
        train_stop = None

    if train_stop is not None:
        # logging.debug('TrainStop found, updating...')
        train_stop.update(train_stop_change)
        db.session.add(train_stop)
        # logging.debug('TrainStop update finished and commited to database')

def set_logging_config():
    logging.basicConfig(filename='test_log.log',
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.DEBUG)


def reset_db(db):
    db.drop_all()
    db.create_tables()


def get_changes(db: DatabaseConnection, timetable: Timetable,
                station: str, request_type: str = 'full'):
    train_stop_changes = timetable.get_changes(station=station, request_type=request_type)

    [update_train_stops_with_changes(db, train_stop_change) for train_stop_change in train_stop_changes]
    db.save_bulk(train_stop_changes, 'bla')


def get_default_time_table(db: DatabaseConnection, timetable: Timetable,
                           station: str, year: int, month: int, day: int, hour: int):
    timetables = timetable.get_default_timetable(station=station,
                                                 year=year,
                                                 month=month,
                                                 day=day,
                                                 hour=hour)
    db.save_bulk(timetables, 'bla')


def get_bahnhof_dict(bahnapi: BahnAPI):
    # stations = ['Köln Hbf', 'Düsseldorf Hbf', 'Duisburg Hbf', 'Essen Hbf', 'Oberhausen Hbf', 'Bochum Hbf',
    #             'Dortmund Hbf', 'Neuss Hbf', 'Krefeld Hbf', 'Mülheim (Ruhr) Hbf', 'Düsseldorf Flughafen',
    #             'Leverkusen Mitte', 'Hamm Hbf', 'Düsseldorf-Benrath', 'Aachen Hbf', 'Wattenscheid',
    #             'Münster Hbf']
    stations = ['Wuppertal Hbf']
    bahnhof_dict = {}
    for station in stations:
        print(station)
        abbrev = bahnapi.get_bahnhof_abbrev(station)
        eva = bahnapi.get_eva_number(abbrev)
        bahnhof_dict[station] = {'abbrev': abbrev,
                                 'eva': eva}
        time.sleep(6.5)

    print(bahnhof_dict)


if __name__ == '__main__':
    main()
