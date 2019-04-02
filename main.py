import time
import logging

import APIRequests
import config.config as config


def main():
    set_logging_config()
    api_requests = APIRequests.APIRequests()

    # get_changes(db, timetable)


def set_logging_config():
    logging.basicConfig(filename='test_log.log',
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.DEBUG)


def get_bahnhof_dict(bahnapi: BahnAPI):
    stations = config.stations
    bahnhof_dict = {}
    for station in stations:
        abbrev = bahnapi.get_bahnhof_abbrev(station)
        eva = bahnapi.get_eva_number(abbrev)
        bahnhof_dict[station] = {'abbrev': abbrev,
                                 'eva': eva}

        # TODO sleeptime into config
        time.sleep(6.5)

    print(bahnhof_dict)


if __name__ == '__main__':
    main()
