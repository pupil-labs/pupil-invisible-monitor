import logging
import typing as T
from contextlib import contextmanager

import glfw.GLFW as glfw
import numpy as np
from pyglui import cygl, ui

from . import gl_utils
from .event_loop import WindowEventLoop
from .observable import Observable

logger = logging.getLogger(__name__)


def normalize(pos, size, flip_y=False):
    """
    normalize return as float
    """
    width, height = size
    x = pos[0]
    y = pos[1]
    x /= float(width)
    y /= float(height)
    if flip_y:
        return x, 1 - y
    return x, y


def denormalize(pos, size, flip_y=False):
    """
    denormalize
    """
    width, height = size
    x = pos[0]
    y = pos[1]
    x *= width
    if flip_y:
        y = 1 - y
    y *= height
    return x, y


class Window(Observable):
    scroll_factor = 10.0

    def __init__(self, texture, frame_rate: float, callables: T.List[T.Callable] = ...):
        if callables is ...:
            callables = []

        self.texture = texture

        callables.insert(0, self.draw_texture)
        self._window = None
        self.event_loop = WindowEventLoop(self, frame_rate, callables)

    @contextmanager
    def use_content_area(self):
        # glViewport to a square centered at the window with maximal size such that it
        # is still fully contained by the windows
        min_size = min(self.window_size)
        x = (self.window_size[0] - min_size) // 2
        y = (self.window_size[1] - min_size) // 2
        rect = (x, y, min_size, min_size)
        with gl_utils.use_viewport(*rect):
            yield rect

    def draw_texture(self):
        if self.is_minimized():
            return

        gl_utils.glClear(gl_utils.GL_COLOR_BUFFER_BIT)
        gl_utils.glClearColor(0, 0, 0, 1)

        with gl_utils.use_norm_based_coordinate_system():
            self.texture.draw()

    def is_minimized(self):
        return (self.window_size is not None) and (0 in self.window_size)

    def update_gui(self):
        with gl_utils.use_viewport(0, 0, *self.window_size):
            user_input = self.gui.update()
            self.process_unconsumed_user_input(user_input)

    def update(self, timeout=0.0):
        glfw.glfwWaitEventsTimeout(timeout)

        self.update_gui()
        gl_utils.glFlush()
        glfw.glfwSwapBuffers(self._window)

        if self.hdpi_changed():
            # calling resize will handle hdpi changes and resize the UI accordingly
            self.manual_resize()

    def hdpi_changed(self):
        return self.hdpi_factor != glfw.glfwGetWindowContentScale(self._window)[0]

    def manual_resize(self):
        self.on_resize(self._window, *glfw.glfwGetFramebufferSize(self._window))

    @property
    def should_draw(self):
        return self._window and not glfw.glfwWindowShouldClose(self._window)

    def open(self, size=(800, 800), pos=(50, 50), gui_scale=1.0, ui_config=None):
        if self._window:
            return

        glfw.glfwInit()
        # Window name needs to be equal to `StartupWMClass` field in Linux .desktop file
        # else the icon will not show correctly on Linux!
        self._window = glfw.glfwCreateWindow(
            *size, "Pupil Invisible Monitor", monitor=None, share=None
        )
        glfw.glfwSetWindowSizeLimits(
            self._window, 200, 200, glfw.GLFW_DONT_CARE, glfw.GLFW_DONT_CARE
        )
        glfw.glfwSetWindowPos(self._window, *pos)
        glfw.glfwMakeContextCurrent(self._window)

        cygl.utils.init()

        self.gui = ui.UI()
        self.gui_user_scale = gui_scale

        # Adding an intermediate container fixes a pylgui display bug
        self.cont = ui.Container((0, 0), (0, 0), (0, 0))
        self.quickbar = ui.Horizontally_Stretching_Menu(
            "Quick Bar", (0.0, -120.0), (0.0, 0.0)
        )
        self.cont.append(self.quickbar)
        self.gui.append(self.cont)

        # Register callbacks main_window
        glfw.glfwSetFramebufferSizeCallback(self._window, self.on_resize)
        glfw.glfwSetKeyCallback(self._window, self.on_window_key)
        glfw.glfwSetCharCallback(self._window, self.on_window_char)
        glfw.glfwSetMouseButtonCallback(self._window, self.on_window_mouse_button)
        glfw.glfwSetCursorPosCallback(self._window, self.on_pos)
        glfw.glfwSetScrollCallback(self._window, self.on_scroll)
        self.gui.configuration = ui_config or {}
        gl_utils.basic_gl_setup()

        # Perform an initial window size setup
        self.manual_resize()

    def close(self):
        if not self._window:
            return

        glfw.glfwRestoreWindow(self._window)

        del self.gui[:]
        self.gui.terminate()
        glfw.glfwDestroyWindow(self._window)
        glfw.glfwTerminate()

        del self.gui
        self._window = None

    def run_event_loop(self):
        self.event_loop.run()

        # Callback functions

    def on_resize(self, window, w, h):
        """Updates windows/UI sizes and redraws the UI with correct HDPI scaling."""

        self.window_size = w, h
        if self.is_minimized():
            return

        # Always clear buffers on resize to make sure that the black stripes left/right
        # are black and not polluted from previous frames. Make sure this is applied on
        # the whole window and not within glViewport!
        gl_utils.glClear(gl_utils.GL_COLOR_BUFFER_BIT)
        gl_utils.glClearColor(0, 0, 0, 1)

        self.hdpi_factor = glfw.glfwGetWindowContentScale(window)[0]
        self.gui.scale = self.gui_user_scale * self.hdpi_factor

        with self.use_content_area() as (x, y, content_w, content_h):
            # update GUI window to full window
            self.gui.update_window(w, h)

            # update content container to content square
            # NOTE: since this is part of the UI, it will be affected by the gui
            # scaling, but we actually need real coordinates, so we need to convert it
            # back.
            self.cont.outline = ui.FitBox(
                ui.Vec2(x // self.hdpi_factor, y // self.hdpi_factor),
                ui.Vec2(content_w // self.hdpi_factor, content_h // self.hdpi_factor),
            )
            self.draw_texture()
            self.gui.collect_menus()
            self.update_gui()

        gl_utils.glFlush()
        glfw.glfwSwapBuffers(self._window)

    def on_window_key(self, window, key, scancode, action, mods):
        self.gui.update_key(key, scancode, action, mods)

    def on_window_char(self, window, char):
        self.gui.update_char(char)

    def on_window_mouse_button(self, window, button, action, mods):
        self.gui.update_button(button, action, mods)

    def on_pos(self, window, x, y):
        self.gui.update_mouse(x, y)

    def on_scroll(self, window, x, y):
        self.gui.update_scroll(x, y * self.scroll_factor)

    def process_unconsumed_user_input(self, user_input):
        if self.is_minimized():
            return
        x, y = glfw.glfwGetCursorPos(self._window)
        pos = x * self.hdpi_factor, y * self.hdpi_factor
        pos = normalize(pos, self.window_size)
        # Position in img pixels
        pos = denormalize(pos, self.texture.shape[:2])
        for button, action, mods in user_input.buttons:
            self.on_click(pos, button, action)

    def on_click(self, pos, button, action):
        pass
