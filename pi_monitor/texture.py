import logging
import numpy as np

logger = logging.getLogger(__name__)


class DebugTextureController:
    def __init__(self):
        self.color = 0
        self.texture = np.zeros((1, 1, 3), dtype=np.uint8)

    def update(self):
        self.texture[:] = self.color
        self.color += 1
        self.color %= 256
