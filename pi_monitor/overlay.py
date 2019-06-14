from pyglui.cygl.utils import RGBA, draw_circle, draw_points


class GazeOverlay:
    size = 70

    def update(self, gaze):
        print(gaze)
        draw_circle(
            center_position=gaze,
            radius=self.size + 75,
            stroke_width=145,
            color=RGBA(0.0, 0.0, 0.0, 0.8),
            sharpness=0.15,
        )
        draw_circle(
            center_position=gaze,
            radius=self.size,
            stroke_width=10,
            color=RGBA(1, 1, 1, 0.6),
            sharpness=0.7,
        )
