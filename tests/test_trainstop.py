from datetime import datetime

import pytest

from TrainStop import TrainStop

import tests.data_tests as data_tests


# TODO rewrite to check object and not dict
@pytest.mark.parametrize('test_input, expected', [
    (data_tests.event_ar, data_tests.event_ar_parsed),
    (data_tests.event_dp, data_tests.event_dp_parsed),
    (data_tests.event_ar_dp, data_tests.event_ar_dp_parsed)
])
def test_eval_default_plan(test_input, expected):
    ts = TrainStop()
    ts.create(test_input, '8000086', 'Duisburg Hbf')
    te = vars(ts)
    te.pop('raw_event')
    te.pop('event_keys')
    te.pop('_sa_instance_state')
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
    assert TrainStop(input_dict, '123', 'Duisburg Hbf')._get_line() == line


@pytest.mark.parametrize('ppth, place', [
    ('a|b|c', 'a'),
    ('', None),
    (None, None),
    ('aa', 'aa')
])
def test_get_departure_place(ppth, place):
    assert TrainStop.get_departure_place(ppth) == place


@pytest.mark.parametrize('ppth, place', [
    ('a|b|c', 'c'),
    ('', None),
    (None, None),
    ('aa', 'aa')
])
def test_get_destination_place(ppth, place):
    assert TrainStop.get_destination_place(ppth) == place


@pytest.mark.parametrize('pt, tstamp', [
    ('1912231234', datetime.strptime('2019-12-23 12:34:00', '%Y-%m-%d %H:%M:%S')),
    ('', None),
    (None, None)
])
def test_get_datetime(pt, tstamp):
    assert TrainStop.get_datetime(pt) == tstamp


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


@pytest.mark.parametrize('raw_event, trainstop_id', [
    (data_tests.event_ar, data_tests.id_event_ar),
    (data_tests.event_dp, data_tests.id_event_dp),
    (data_tests.event_ar_dp, data_tests.id_event_ar_dp)
])
def test_get_id(raw_event, trainstop_id):
    ts = TrainStop(raw_event, '123', 'asd')
    ts.get_id()
    assert ts.trainstop_id == trainstop_id


@pytest.mark.parametrize('raw_event, train_stop_dict', [
    (data_tests.event_ar, data_tests.event_ar_parsed),
    (data_tests.event_dp, data_tests.event_dp_parsed),
    (data_tests.event_ar_dp, data_tests.event_ar_dp_parsed)
])
def test_convert_to_dict(raw_event, train_stop_dict):
    ts = TrainStop(raw_event, '8000086', 'Duisburg Hbf')
    assert ts.convert_to_dict() == train_stop_dict
