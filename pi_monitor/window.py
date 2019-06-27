import logging
import typing as T

from pyglui import ui, cygl

from . import gl_utils
from . import glfw
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

    def draw_texture(self):
        gl_utils.glViewport(0, 0, *self.window_size)
        gl_utils.glFlush()
        gl_utils.make_coord_system_norm_based()
        logger.debug("draw()")
        self.texture.draw()
        gl_utils.make_coord_system_pixel_based(self.texture.shape)

    def update_gui(self):
        try:
            clipboard = glfw.glfwGetClipboardString(self._window).decode()
        except AttributeError:  # clipbaord is None, might happen on startup
            clipboard = ""
        self.gui.update_clipboard(clipboard)
        user_input = self.gui.update()
        self.process_unconsumed_user_input(user_input)
        if user_input.clipboard and user_input.clipboard != clipboard:
            # only write to clipboard if content changed
            glfw.glfwSetClipboardString(self._window, user_input.clipboard.encode())

    def update(self, timeout=0.0):
        glfw.glfwWaitEventsTimeout(timeout)
        logger.debug("update_gui")
        self.update_gui()
        logger.debug("swapping")
        glfw.glfwSwapBuffers(self._window)
        logger.debug("swapped")

    @property
    def should_draw(self):
        return self._window and not glfw.glfwWindowShouldClose(self._window)

    def open(self, size=(800, 800), pos=(50, 50), gui_scale=1.0, ui_config=None):
        if self._window:
            return

        glfw.glfwInit()
        glfw.glfwWindowHint(glfw.GLFW_RESIZABLE, False)
        self._window = glfw.glfwCreateWindow(*size, "PI Monitor")
        glfw.glfwSetWindowPos(self._window, *pos)
        glfw.glfwMakeContextCurrent(self._window)

        cygl.utils.init()

        self.gui = ui.UI()
        self.gui_user_scale = gui_scale

        self.quickbar = ui.Horizontally_Stretching_Menu(
            "Quick Bar", (100, 680), (-100, 120)
        )
        self.gui.append(self.quickbar)

        # Register callbacks main_window
        glfw.glfwSetFramebufferSizeCallback(self._window, self.on_resize)
        glfw.glfwSetKeyCallback(self._window, self.on_window_key)
        glfw.glfwSetCharCallback(self._window, self.on_window_char)
        glfw.glfwSetMouseButtonCallback(self._window, self.on_window_mouse_button)
        glfw.glfwSetCursorPosCallback(self._window, self.on_pos)
        glfw.glfwSetScrollCallback(self._window, self.on_scroll)
        self.gui.configuration = ui_config or {}
        gl_utils.basic_gl_setup()

        self.on_resize(self._window, *glfw.glfwGetFramebufferSize(self._window))

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
        self.window_size = w, h
        self.hdpi_factor = glfw.getHDPIFactor(window)
        self.gui.scale = self.gui_user_scale * self.hdpi_factor
        self.gui.update_window(w, h)
        self.gui.collect_menus()

    def on_window_key(self, window, key, scancode, action, mods):
        self.gui.update_key(key, scancode, action, mods)

    def on_window_char(self, window, char):
        self.gui.update_char(char)

    def on_window_mouse_button(self, window, button, action, mods):
        self.gui.update_button(button, action, mods)

    def on_pos(self, window, x, y):
        x, y = x * self.hdpi_factor, y * self.hdpi_factor
        self.gui.update_mouse(x, y)

    def on_scroll(self, window, x, y):
        self.gui.update_scroll(x, y * self.scroll_factor)

    def set_scale(self, new_scale):
        self.gui_user_scale = new_scale
        self.on_resize(self._window, *self.window_size)

    def process_unconsumed_user_input(self, user_input):
        x, y = glfw.glfwGetCursorPos(self._window)
        pos = x * self.hdpi_factor, y * self.hdpi_factor
        pos = normalize(pos, self.window_size)
        # Position in img pixels
        pos = denormalize(pos, self.texture.shape[:2])
        for button, action, mods in user_input.buttons:
            self.on_click(pos, button, action)

    def on_click(self, pos, button, action):
        pass
