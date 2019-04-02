from datetime import datetime, timedelta
import heapq


class RequestsHeap:
    def __init__(self):
        self.requests_heap = []
        # TODO move limit_requests_heap and event_lifetime to config
        self.event_lifetime = 130
        self.limit_requests_heap = 20

    def append_event(self):
        self.requests_heap.append(datetime.now() + timedelta(seconds=self.event_lifetime))

    def check_requests_heap(self):
        self._remove_expired_requests()

        if len(self.requests_heap) < self.limit_requests_heap:
            return True

    def _remove_expired_requests(self):
        while True:
            if len(self.requests_heap) == 0 or (self.requests_heap[0] - datetime.now()).total_seconds() < 0:
                return
            else:
                heapq.heappop(self.requests_heap)
