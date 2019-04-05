from datetime import datetime, timedelta
import heapq


class RequestsHeap:
    def __init__(self):
        self.heap = []
        # TODO move limit_requests_heap and event_lifetime to config
        self.seconds_event_lifetime = 125
        self.limit_requests_heap = 20

    def append_event(self):
        self.heap.append(datetime.now() + timedelta(seconds=self.seconds_event_lifetime))

    def get_available_requests(self) -> int:
        self._remove_expired_requests()

        return self.limit_requests_heap - len(self.heap)

    def _remove_expired_requests(self):
        while True:
            if len(self.heap) == 0 or self.get_age_oldest_request() > 0:
                return
            else:
                heapq.heappop(self.heap)

    def get_age_oldest_request(self) -> int:
        return (self.heap[0] - datetime.now()).total_seconds()
