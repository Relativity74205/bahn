import time

from sqlalchemy.exc import SQLAlchemyError

import DatabaseConnection as dc
import BahnAPI
import Timetable
from TrainStop import TrainStop


if __name__ == '__main__':
    db = dc.DatabaseConnection()
    # db.drop_all()
    # db.create_tables()

    ba = BahnAPI.BahnAPI()

    timetable = Timetable.Timetable(ba)
    list_trainstops = timetable.get_default_timetable(station='Duisburg Hbf',
                                                      year=2019,
                                                      month=3,
                                                      day=11,
                                                      hour=14)
    # try:
    #     db.save_bulk(list_trainstops, 'TrainStops')
    # except SQLAlchemyError as e:
    #     if 'constraint failed' in str(e):
    #         print('at least one dataset already in DB, switching to fallback')
    #         # TODO create fallback function (instead of bulk insert, insert single line and looking before)
    #     else:
    #         print('else DB error')

    test2 = db.get_by_pk(TrainStop, '2678604870744955109-1903111357-5')
    test2 = db.get_by_pk(TrainStop, 'asd')
    print(test2)


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
