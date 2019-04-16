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
    # db = DatabaseConnection.DatabaseConnection()
    # db.reset_db()

    ba = BahnAPI.BahnAPI()

    # timetable = Timetable.Timetable(ba)
    # timetables = get_default_time_table(timetable, 'Duisburg Hbf', 2019, 3, 30, 24)
    # get_changes(timetable, 'Duisburg Hbf', 'full')
    # get_changes(timetable, 'Duisburg Hbf', 'recent'))
    get_bahnhof_dict(ba)


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

    db.save_bulk(train_stop_changes)


def get_default_time_table(db: DatabaseConnection, timetable: Timetable,
                           station: str, year: int, month: int, day: int, hour: int):
    timetables = timetable.get_default_timetable(station=station,
                                                 year=year,
                                                 month=month,
                                                 day=day,
                                                 hour=hour)
    db.save_bulk(timetables)


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
