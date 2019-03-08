import DatabaseConnection as dc
import BahnAPI
import Timetable
import TrainStop


if __name__ == '__main__':
    db = dc.DatabaseConnection()
    db.drop_all()
    db.create_tables()

    ba = BahnAPI.BahnAPI()

    timetable = Timetable.Timetable(ba)
    list_trainstops = timetable.get_default_timetable(station='Duisburg Hbf',
                                                      year=2019,
                                                      month=3,
                                                      day=8,
                                                      hour=23)

    db.save_bulk(list_trainstops, 'TrainStops')


