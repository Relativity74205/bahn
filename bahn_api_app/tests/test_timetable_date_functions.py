import pytest
from datetime import datetime

from project import timetable_date_functions as tdf


@pytest.mark.parametrize("last_datehour, last_time", [
    ('2019010101', datetime(2019, 1, 1, 1)),
    ('2019010100', datetime(2019, 1, 1, 0)),
    ('2019111', datetime(2019, 1, 1, 1))
])
def test_get_last_default_plan_time(last_datehour, last_time):
    assert tdf.get_last_default_plan_time(last_datehour) == last_time


@pytest.mark.parametrize("last_time, amount_missing_dates, missing_dates", [
    (datetime(2019, 1, 1, 1), 1, [(2019, 1, 1, 2)]),
    (datetime(2019, 1, 1, 1), 3, [(2019, 1, 1, 2),
                                  (2019, 1, 1, 3),
                                  (2019, 1, 1, 4)]),
    (datetime(2019, 1, 1, 1), 0, [])
])
def test_generate_missing_dates(last_time, amount_missing_dates, missing_dates):
    assert tdf.generate_missing_dates(last_time, amount_missing_dates) == missing_dates


@pytest.mark.parametrize("missing_dates, missing_dates_tuple", [
    ([datetime(2019, 1, 1, 1)], [(2019, 1, 1, 1)]),
    ([datetime(2019, 1, 1, 1), datetime(2019, 1, 1, 2), datetime(2019, 1, 1, 3)],
     [(2019, 1, 1, 1), (2019, 1, 1, 2), (2019, 1, 1, 3)]),
    ([], [])
])
def test_convert_missing_dates(missing_dates, missing_dates_tuple):
    assert tdf.convert_missing_dates(missing_dates) == missing_dates_tuple


@pytest.mark.parametrize("current_time, last_datehour, missing_dates", [
    (datetime(2019, 3, 15, 18, 12, 12), '2019031518', tdf.generate_missing_dates(datetime(2019, 3, 15, 18), 12)),
    (datetime(2019, 3, 15, 18, 12, 12), '2019031519', tdf.generate_missing_dates(datetime(2019, 3, 15, 19), 11)),
    (datetime(2019, 3, 15, 18, 12, 12), None, tdf.generate_missing_dates(datetime(2019, 3, 15, 17), 13))
])
def test_get_missing_default_plan_dates(current_time, last_datehour, missing_dates):
    a = tdf.get_missing_default_plan_dates(current_time, last_datehour)
    assert a == missing_dates
