import logging
from .models import Host_Controller
from .overlay import GazeOverlay
from .texture import PITextureController
from .ui import Thumb_Controller
from .window import Window

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("pyre").setLevel(logging.WARNING)

try:
    gaze_overlay = GazeOverlay()
    host_controller = Host_Controller()
    texture_controller = PITextureController()
    # frame observer
    host_controller.add_observer("on_host_linked", texture_controller.reset)
    host_controller.add_observer("on_recent_frame", texture_controller.update)
    host_controller.add_observer("on_recent_gaze", gaze_overlay.update)

    win = Window(
        texture_controller,
        frame_rate=60.0,
        callables=[host_controller.poll_events, host_controller.fetch_recent_data],
    )
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
