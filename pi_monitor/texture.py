import logging
from pathlib import Path

import numpy as np
import cv2

from pyglui.cygl.utils import Named_Texture

logger = logging.getLogger(__name__)


class PITextureController:
    def _initialize(self):
        self._texture = Named_Texture()
        self.reset()

    def update(self, frame):
        if frame.yuv_buffer is not None:
            self._texture.update_from_yuv_buffer(
                frame.yuv_buffer, frame.width, frame.height
            )
            self.shape = frame.height, frame.width, 3
        else:
            self._texture.update_from_ndarray(frame.bgr)
            self.shape = frame.bgr.shape

    def draw(self):
        try:
            self._texture.draw()
        except AttributeError:
            self._initialize()
            self._texture.draw()

    def reset(self):
        ph_path = Path(__file__).parent / "placeholder.png"
        ph_bgr = cv2.imread(str(ph_path))
        self._texture.update_from_ndarray(ph_bgr)
        self.shape = ph_bgr.shape
