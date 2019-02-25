import pytest

from BahnAPI import BahnAPI
from Timetable import Timetable

import tests.data_tests as data_tests


@pytest.fixture
def tt():
    ba = BahnAPI()
    return Timetable(ba)


def test_get_default_plan_json(tt):
    assert False


def test_get_default_plan(tt):
    assert False


@pytest.mark.parametrize("station, eva", [
    ('', None),
    ('Duisburg Hbf', '8000086')
])
def test_get_eva(tt, station, eva):
    assert tt._get_eva(station) == eva


@pytest.mark.parametrize("year, month, day, date", [
    (2019, 12, 25, '191225'),
    (2019, 1, 1, '190101'),
    (19, 1, 1, '190101'),
    (2001, 0, 0, '010000')
])
def test_get_date(year, month, day, date):
    assert Timetable._get_date(year, month, day) == date


@pytest.mark.parametrize("hour_int, hour_str", [
    (24, '24'),
    (9, '09'),
    (0, '00')
])
def test_get_hour(hour_int, hour_str):
    assert Timetable._get_hour(hour_int) == hour_str


def test_get_departure_place():
    ppth = 'a|b|c'
    assert get_departure_place(ppth) == 'a'
    assert not get_departure_place('')


def test_get_destination_place():
    ppth = 'a|b|c'
    assert get_destination_place(ppth) == 'c'
    assert not get_destination_place('')


def test_get_date():
    pt = '1912231234'
    assert get_date(pt) == '2019-12-23'
    assert not get_date('')


def test_get_time():
    pt = '1912231234'
    assert get_time(pt) == '12:34'
    assert not get_time('')


def test_get_train_number():
    assert get_train_number('RE19', 'RE') == 'RE19'
    assert get_train_number('3', 'S') == 'S3'


@pytest.mark.parametrize("test_input, expected", [
    ({'tl': {'@c': 'ICE', '@n': '100'}, 'ar': {'p': '2'}, 'dp': {'p': '2'}}, 'ICE100'),
    ({'tl': {'@c': 'S', '@n': '1234'}, 'ar': {'p': '2', '@l': '2'}}, 'S2'),
    ({'tl': {'@c': 'S', '@n': '1234'}, 'dp': {'p': '2', '@l': '2'}}, 'S2'),
    ({'tl': {'@c': 'S', '@n': '1234'}, 'ar': {'p': '2', '@l': 2}}, 'S2'),
    ({'tl': {'@c': 'ABR', '@n': '1234'}, 'ar': {'p': '2', '@l': 'RE19'}}, 'RE19')
])
def test_get_line(test_input, expected):
    assert get_line(test_input) == expected


@pytest.mark.parametrize("test_input, expected", [
    (data_tests.event_ar, data_tests.event_ar_parsed),
    (data_tests.event_dp, data_tests.event_dp_parsed),
    (data_tests.event_ar_dp, data_tests.event_ar_dp_parsed)
])
def test_eval_default_plan(test_input, expected):
    assert eval_default_plan(test_input, 'Duisburg Hbf') == expected
