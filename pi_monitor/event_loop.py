import logging
import time
import typing as T
import weakref

logger = logging.getLogger(__name__)

MIN_WAIT_TIME = 0.0001


class WindowEventLoop:
    def __init__(self, window, frame_rate: float, callables: T.List[T.Callable]):
        self.window = weakref.ref(window)
        self.target_loop_duration = 1 / frame_rate
        self.callables = callables
        self.last_sleep = None

    def run(self):
        while self.window().should_draw:
            self.update()
            time_to_wait = MIN_WAIT_TIME
            if self.last_sleep:
                loop_duration = time.monotonic() - self.last_sleep
                time_to_wait = max(
                    time_to_wait, self.target_loop_duration - loop_duration
                )
            self.window().update(time_to_wait)
            self.last_sleep = time.monotonic()

    def update(self):
        for call in self.callables:
            call()
