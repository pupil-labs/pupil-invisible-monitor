import logging.handlers
from pathlib import Path

from .filter import OffsetFilter
from .models import Host_Controller
from .overlay import GazeOverlay
from .texture import PITextureController
from .ui import HostViewController, OffsetFilterViewController
from .window import Window


def main():
    log_path = Path.home() / "pi_monitor_settings" / "pi_monitor.log"
    log_path.parent.mkdir(exist_ok=True)
    handlers = [
        logging.StreamHandler(),
        logging.handlers.RotatingFileHandler(log_path, mode="w", backupCount=30),
    ]
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=handlers,
        style="{",
        format="{asctime} [{levelname}] {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("pyre").setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)

    try:
        host_controller = Host_Controller()

        offset_filter = OffsetFilter()
        host_controller.add_observer("on_recent_gaze", offset_filter.filter_gaze)

        # frame observer
        texture_controller = PITextureController()
        host_controller.add_observer("on_host_linked", texture_controller.reset)
        host_controller.add_observer("on_recent_frame", texture_controller.update)

        gaze_overlay = GazeOverlay()
        offset_filter.add_observer("on_filtered_gaze", gaze_overlay.update)

        win = Window(
            texture_controller,
            frame_rate=60.0,
            callables=[
                host_controller.poll_events,
                host_controller.fetch_recent_data,
                gaze_overlay.draw,
            ],
        )
        win.open()
        offset_filter_view_controller = OffsetFilterViewController(
            gui_parent=win.gui, controller=offset_filter
        )
        win.add_observer("on_click", offset_filter_view_controller.on_click)
        host_view_controller = HostViewController(
            gui_parent=win.quickbar, controller=host_controller
        )

        win.run_event_loop()
    except KeyboardInterrupt:
        pass
    except Exception:
        logger.exception("Exception occured!")
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.handlers.RotatingFileHandler):
                handler.doRollover()
    finally:
        win.close()
        host_controller.cleanup()
        host_view_controller.cleanup()
        offset_filter_view_controller.cleanup()
        logging.shutdown()


if __name__ == "__main__":
    main()
