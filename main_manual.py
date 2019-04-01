import time
import logging

import DatabaseConnection as dc
import BahnAPI
import Timetable


def main():
    set_logging_config()
    db = dc.DatabaseConnection()
    # reset_db(db)

    ba = BahnAPI.BahnAPI()

    timetable = Timetable.Timetable(ba, db)
    get_default_time_table(timetable, 'Duisburg Hbf', 2019, 3, 30, 24)
    # get_changes(timetable, 'Duisburg Hbf', 'full')
    # get_changes(timetable, 'Duisburg Hbf', 'recent')


def set_logging_config():
    logging.basicConfig(filename='test_log.log',
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.DEBUG)


def reset_db(db):
    db.drop_all()
    db.create_tables()


def get_changes(timetable: Timetable, station: str, request_type: str = 'full'):
    _ = timetable.get_changes(station=station, request_type=request_type)


def get_default_time_table(timetable: Timetable, station: str, year: int, month: int, day: int, hour: int):
    _ = timetable.get_default_timetable(station=station,
                                        year=year,
                                        month=month,
                                        day=day,
                                        hour=hour)


def get_bahnhof_dict(bahnapi: BahnAPI):
    stations = ['Köln Hbf', 'Düsseldorf Hbf', 'Duisburg Hbf', 'Essen Hbf', 'Oberhausen Hbf', 'Bochum Hbf', 'Dortmund Hbf',
                'Neuss Hbf', 'Krefeld Hbf', 'Mülheim (Ruhr) Hbf', 'Düsseldorf Flughafen']
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
