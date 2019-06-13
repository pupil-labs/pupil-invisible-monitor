import logging
import time
import typing as T
import weakref

logger = logging.getLogger(__name__)


class WindowEventLoop:
    def __init__(self, window, frame_rate: float, callables: T.List[T.Callable]):
        self.window = weakref.ref(window)
        self.target_loop_duration = 1 / frame_rate
        self.callables = callables
        self.last_sleep = None

    def run(self):
        while self.window().should_draw:
            self.update()
            if self.last_sleep:
                loop_duration = time.monotonic() - self.last_sleep
                if loop_duration < self.target_loop_duration:
                    time.sleep(self.target_loop_duration - loop_duration)
            self.last_sleep = time.monotonic()
            self.window().draw()

    def update(self):
        for call in self.callables:
            call()
