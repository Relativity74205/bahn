import pytest

from BahnAPI import BahnAPI
from Timetable import Timetable


@pytest.fixture
def tt():
    ba = BahnAPI()
    return Timetable(ba)


def test_get_timetable_json(tt):
    assert False


def test_get_default_timetable(tt):
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
