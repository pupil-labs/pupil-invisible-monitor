import logging
import sys
from pathlib import Path

import numpy as np

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
        placeholder = np.ones((1080, 1088, 3), dtype=np.uint8) * 158
        self._texture.update_from_ndarray(placeholder)
        self.shape = placeholder.shape
