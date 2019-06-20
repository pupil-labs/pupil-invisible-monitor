from pyglui.cygl.utils import RGBA, draw_circle, draw_points


class GazeOverlay:
    def __init__(self, ring_size=70):
        self.ring_size = 70
        self._recent_gaze = None

    def draw(self):
        if self._recent_gaze:
            draw_circle(
                center_position=self._recent_gaze,
                radius=self.ring_size + 75,
                stroke_width=145,
                color=RGBA(0.0, 0.0, 0.0, 0.8),
                sharpness=0.15,
            )
            draw_circle(
                center_position=self._recent_gaze,
                radius=self.ring_size,
                stroke_width=10,
                color=RGBA(1, 1, 1, 0.6),
                sharpness=0.7,
            )

    def update(self, gaze):
        self._recent_gaze = gaze
