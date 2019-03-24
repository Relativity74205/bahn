import time
import logging

from sqlalchemy.exc import SQLAlchemyError

import DatabaseConnection as dc
import BahnAPI
import Timetable


def main():
    set_logging_config()
    db = dc.DatabaseConnection()
    reset_db(db)

    ba = BahnAPI.BahnAPI()

    timetable = Timetable.Timetable(ba, db)
    get_default_time_table(db, timetable)
    # get_changes(db, timetable)


def set_logging_config():
    logging.basicConfig(filename='test_log.log',
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.DEBUG)


def reset_db(db):
    db.drop_all()
    db.create_tables()


def get_changes(db: dc.DatabaseConnection, timetable: Timetable):
    list_trainstopchanges = timetable.get_changes(station='Duisburg Hbf')

    try:
        db.save_bulk(list_trainstopchanges, 'TrainStopChanges')
    except SQLAlchemyError as e:
        if 'constraint failed' in str(e):
            print('at least one dataset already in DB, switching to fallback')
            # TODO create fallback function (instead of bulk insert, insert single line and looking before)
        else:
            print('else DB error')


def get_default_time_table(db: dc.DatabaseConnection, timetable: Timetable):
    list_trainstops = timetable.get_default_timetable(station='Duisburg Hbf',
                                                      year=2019,
                                                      month=3,
                                                      day=24,
                                                      hour=21)

    try:
        db.save_bulk(list_trainstops, 'TrainStops')
    except SQLAlchemyError as e:
        if 'constraint failed' in str(e):
            print('at least one dataset already in DB, switching to fallback')
            # TODO create fallback function (instead of bulk insert, insert single line and looking before)
        else:
            print('else DB error')


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
