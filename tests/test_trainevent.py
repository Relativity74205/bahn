import pytest

from TrainEvent import TrainEvent

import tests.data_tests as data_tests


@pytest.mark.parametrize("test_input, expected", [
    (data_tests.event_ar, data_tests.event_ar_parsed),
    (data_tests.event_dp, data_tests.event_dp_parsed),
    (data_tests.event_ar_dp, data_tests.event_ar_dp_parsed)
])
def test_eval_default_plan(test_input, expected):
    te = vars(TrainEvent(test_input, 'Duisburg Hbf'))
    te.pop('raw_event')
    te.pop('event_keys')
    assert te == expected


def test_get_train_number():
    assert TrainEvent._get_train_number('RE19', 'RE') == 'RE19'
    assert TrainEvent._get_train_number('3', 'S') == 'S3'


@pytest.mark.parametrize("test_input, expected", [
    ({'tl': {'@c': 'ICE', '@n': '100'}, 'ar': {'p': '2'}, 'dp': {'p': '2'}}, 'ICE100'),
    ({'tl': {'@c': 'S', '@n': '1234'}, 'ar': {'p': '2', '@l': '2'}}, 'S2'),
    ({'tl': {'@c': 'S', '@n': '1234'}, 'dp': {'p': '2', '@l': '2'}}, 'S2'),
    ({'tl': {'@c': 'S', '@n': '1234'}, 'ar': {'p': '2', '@l': 2}}, 'S2'),
    ({'tl': {'@c': 'ABR', '@n': '1234'}, 'ar': {'p': '2', '@l': 'RE19'}}, 'RE19')
])
def test_get_line(test_input, expected):
    assert TrainEvent(test_input, 'Duisburg Hbf')._get_line() == expected


def test_get_departure_place():
    ppth = 'a|b|c'
    assert TrainEvent._get_departure_place(ppth) == 'a'
    assert not TrainEvent._get_departure_place('')
    assert not TrainEvent._get_departure_place(None)


def test_get_destination_place():
    ppth = 'a|b|c'
    assert TrainEvent._get_destination_place(ppth) == 'c'
    assert not TrainEvent._get_destination_place('')
    assert not TrainEvent._get_destination_place(None)


def test_get_date():
    pt = '1912231234'
    assert TrainEvent._get_date(pt) == '2019-12-23'
    assert not TrainEvent._get_date('')
    assert not TrainEvent._get_date(None)


def test_get_time():
    pt = '1912231234'
    assert TrainEvent._get_time(pt) == '12:34'
    assert not TrainEvent._get_time('')
    assert not TrainEvent._get_time(None)