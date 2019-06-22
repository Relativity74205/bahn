import unittest.mock as mock

import pytest

from project.APIRequests import APIRequests
from project.RequestsHeap import RequestsHeap
from project.DatabaseConnection import DatabaseConnection
from project.Timetable import Timetable
import config.config as config


def test_apirequests():
    with mock.patch('project.APIRequests.APIRequests._init_last_update') as last_update_mocked:
        apirequest = APIRequests()

        assert isinstance(apirequest.requests_heap, RequestsHeap)
        assert isinstance(apirequest.db, DatabaseConnection)
        assert isinstance(apirequest.timetable, Timetable)
        assert apirequest.stations == config.stations
        assert apirequest.recent_request_lifetime
        assert apirequest.hours_between_updates
        assert apirequest.sleep_time_between_loops
        assert apirequest.max_default_plans
        assert apirequest.min_seconds_between_requests
        assert apirequest.last_complete_update == {'default': None,
                                                   'full': None}

        last_update_mocked.assert_called()


@pytest.mark.parametrize('stations', [
    [],
    ['a', 'b']
])
def test_apirequest_init_last_update(stations):
    apirequest = APIRequests()
    apirequest.stations = stations
    last_single_update = apirequest._init_last_update()
    for station in stations:
        assert last_single_update[station] == {'default': None,
                                               'full': None,
                                               'recent': None}


def test_apirequest_main_loop():
    assert False


def test_apirequest_wait_for_available_requests():
    assert False


def test_apirequest_load_next():
    assert False


def test_apirequest_get_default_tables():
    assert False


def test_apirequest_get_update():
    assert False


def test_apirequest_get_single_update():
    assert False


def test_apirequest_short_time_since_last_update():
    assert False


@pytest.mark.parametrize('sleep_type, sleep_time, sleep_called', [
    ('loop_iteration_ended', 1, True),
    ('short_time_since_last_update', 1, True),
    ('short_time_since_last_update', -1, False),
])
def test_apirequest_sleep(sleep_type, sleep_time, sleep_called):
    with mock.patch('time.sleep') as sleep_mocked:
        APIRequests.sleep(sleep_type, sleep_time)
        if sleep_called:
            sleep_mocked.assert_called_with(sleep_time)
        else:
            sleep_mocked.assert_not_called()


def test_apirequest_save_data():
    assert False
