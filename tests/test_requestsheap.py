import pytest
import time
from datetime import datetime, timedelta

import RequestsHeap


@pytest.fixture
def requests_heap():
    requests_heap = RequestsHeap.RequestsHeap()
    requests_heap.event_lifetime = 0.1
    requests_heap.limit_requests_heap = 3

    return requests_heap


def test_requests_heap(requests_heap):
    assert len(requests_heap.heap) == 0
    assert requests_heap.event_lifetime
    assert requests_heap.limit_requests_heap


def test_requests_heap_append_event(requests_heap):
    requests_heap.append_event()
    assert len(requests_heap.heap) == 1
    assert (requests_heap.heap[0] - datetime.now()).total_seconds() == requests_heap.event_lifetime
    requests_heap.append_event()
    requests_heap.append_event()
    assert len(requests_heap.heap) == 3


def test_requests_heap_check_requests_heap(requests_heap):
    assert requests_heap.check_requests_heap()
    requests_heap.append_event()
    requests_heap.append_event()
    requests_heap.append_event()
    assert not requests_heap.check_requests_heap()
    time.sleep(0.1)
    assert requests_heap.check_requests_heap()


def test_requests_heap_remove_expired_requests(requests_heap):
    requests_heap._remove_expired_requests()
    assert len(requests_heap.heap) == 0
    requests_heap.append_event()
    assert len(requests_heap.heap) == 1
    time.sleep(0.1)
    requests_heap.append_event()
    requests_heap.append_event()
    assert len(requests_heap.heap) == 3
    time.sleep(requests_heap.event_lifetime - 0.1 + 0.01)
    requests_heap._remove_expired_requests()
    assert len(requests_heap.heap) == 2
    time.sleep(0.3)
    requests_heap._remove_expired_requests()
    assert len(requests_heap.heap) == 0
