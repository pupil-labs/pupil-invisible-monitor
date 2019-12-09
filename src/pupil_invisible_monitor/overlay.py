from pyglui.cygl.utils import RGBA, draw_circle, draw_points

from . import gl_utils


class GazeOverlay:
    def __init__(self, ring_size=160):
        self.ring_size = ring_size
        self._recent_gaze = None

    def draw(self):
        if self._recent_gaze:
            # incoming gaze data is in rect(0, 0, 1088, 1080)
            with gl_utils.use_coordinate_system(0, 1088, 1080, 0):
                draw_circle(
                    center_position=self._recent_gaze,
                    radius=self.ring_size,
                    stroke_width=30,
                    color=RGBA(1.0, 0.0, 0.0, 0.6),
                    sharpness=0.8,
                )

    def update(self, gaze):
        self._recent_gaze = gaze
