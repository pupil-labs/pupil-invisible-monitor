import logging
from .models import Host_Controller
from .ui import Thumb_Controller
from .texture import DebugTextureController
from .window import Window

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("pyre").setLevel(logging.WARNING)

try:
    host_controller = Host_Controller()
    texture_controller = DebugTextureController()

    win = Window(
        60.0, callables=[host_controller.poll_events, texture_controller.update]
    )
    win.texture = texture_controller.texture
    win.open()
    thumb_controller = Thumb_Controller(
        gui_parent=win.quickbar, controller=host_controller
    )

    win.run_event_loop()
except KeyboardInterrupt:
    pass
finally:
    win.close()
    host_controller.cleanup()
    thumb_controller.cleanup()
