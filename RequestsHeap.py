from datetime import datetime, timedelta
import heapq


class RequestsHeap:
    def __init__(self):
        self.heap = []
        # TODO move limit_requests_heap and event_lifetime to config
        self.event_lifetime = 130
        self.limit_requests_heap = 20

    def append_event(self):
        self.heap.append(datetime.now() + timedelta(seconds=self.event_lifetime))

    def check_requests_heap(self):
        self._remove_expired_requests()

        if len(self.heap) < self.limit_requests_heap:
            return True
        else:
            return False

    def _remove_expired_requests(self):
        while True:
            if len(self.heap) == 0 or (self.heap[0] - datetime.now()).total_seconds() > 0:
                return
            else:
                heapq.heappop(self.heap)
