from datetime import datetime

import pytest

from TrainStop import TrainStop

import tests.data_tests as data_tests


@pytest.mark.parametrize("test_input, expected", [
    (data_tests.event_ar, data_tests.event_ar_parsed),
    (data_tests.event_dp, data_tests.event_dp_parsed),
    (data_tests.event_ar_dp, data_tests.event_ar_dp_parsed)
])
def test_eval_default_plan(test_input, expected):
    te = vars(TrainStop(test_input, 'Duisburg Hbf'))
    te.pop('raw_event')
    te.pop('event_keys')
    assert te == expected


@pytest.mark.parametrize('number, train_type, train_number', [
    ('RE19', 'RE', 'RE19'),
    ('3', 'S', 'S3')
])
def test_get_train_number(number, train_type, train_number):
    assert TrainStop._get_train_number(number, train_type) == train_number


@pytest.mark.parametrize('input_dict, line', [
    ({'tl': {'@c': 'ICE', '@n': '100'}, 'ar': {'p': '2'}, 'dp': {'p': '2'}}, 'ICE100'),
    ({'tl': {'@c': 'S', '@n': '1234'}, 'ar': {'p': '2', '@l': '2'}}, 'S2'),
    ({'tl': {'@c': 'S', '@n': '1234'}, 'dp': {'p': '2', '@l': '2'}}, 'S2'),
    ({'tl': {'@c': 'S', '@n': '1234'}, 'ar': {'p': '2', '@l': 2}}, 'S2'),
    ({'tl': {'@c': 'ABR', '@n': '1234'}, 'ar': {'p': '2', '@l': 'RE19'}}, 'RE19')
])
def test_get_line(input_dict, line):
    assert TrainStop(input_dict, 'Duisburg Hbf')._get_line() == line


@pytest.mark.parametrize('ppth, place', [
    ('a|b|c', 'a'),
    ('', None),
    (None, None),
    ('aa', 'aa')
])
def test_get_departure_place(ppth, place):
    assert TrainStop._get_departure_place(ppth) == place


@pytest.mark.parametrize('ppth, place', [
    ('a|b|c', 'c'),
    ('', None),
    (None, None),
    ('aa', 'aa')
])
def test_get_destination_place(ppth, place):
    assert TrainStop._get_destination_place(ppth) == place


@pytest.mark.parametrize('pt, tstamp', [
    ('1912231234', datetime.strptime('2019-12-23 12:34:00', '%Y-%m-%d %H:%M:%S')),
    ('', None),
    (None, None)
])
def test_get_datetime(pt, tstamp):
    assert TrainStop._get_datetime(pt) == tstamp


@pytest.mark.parametrize('pt, datestr', [
    ('1912231234', '2019-12-23'),
    ('', None),
    (None, None)
])
def test_get_date(pt, datestr):
    assert TrainStop._get_datestr(pt) == datestr


@pytest.mark.parametrize('pt, timestr', [
    ('1912231234', '12:34:00'),
    ('', None),
    (None, None)
])
def test_get_time(pt, timestr):
    assert TrainStop._get_timestr(pt) == timestr


def test_get_id():
    assert False


def test_get_value():
    assert False


def test_convert_to_dict():
    assert False
