from .observable import Observable


class OffsetFilter(Observable):
    def __init__(self, offset=(0.0, 0.0)):
        self.offset = offset
        self._recent_unfiltered_gaze = offset

    def filter_gaze(self, gaze):
        self._recent_unfiltered_gaze = gaze
        gaze = (gaze[0] + self.offset[0], gaze[1] + self.offset[1])
        self.on_filtered_gaze(gaze)

    def on_filtered_gaze(self, gaze):
        pass

    def update_offset(self, pos):
        x = pos[0] - self._recent_unfiltered_gaze[0]
        y = pos[1] - self._recent_unfiltered_gaze[1]
        self.offset = x, y
