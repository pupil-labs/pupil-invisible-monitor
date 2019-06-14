import logging
from pyglui import ui

from .models import Host_Controller

logger = logging.getLogger(__name__)


class Thumb_Controller:
    def __init__(self, gui_parent, controller: Host_Controller):
        self.gui_parent = gui_parent
        controller.add_observer("on_host_added", self.on_host_added)
        controller.add_observer("on_host_removed", self.on_host_removed)
        controller.add_observer("on_host_changed", self.on_host_changed)
        self.controller = controller

    def on_host_added(self, host_idx):
        logger.debug(f"on_host_added({host_idx})")
        host = self.controller[host_idx]
        host_thumb = self.thumb_for_host(host)
        self.gui_parent.insert(host_idx, host_thumb)

    def on_host_removed(self, host_idx):
        logger.debug(f"on_host_removed({host_idx})")
        del self.gui_parent[host_idx]

    def on_host_changed(self, host_idx):
        logger.debug(f"on_host_changed({host_idx})")
        host = self.controller[host_idx]
        thumb = self.gui_parent[host_idx]
        if host.is_linked and host.is_available:
            thumb.on_color[:] = (0.0, 1.0, 0.0, 0.8)
            thumb.status_text = " "
        elif host.is_linked and not host.is_available:
            thumb.on_color[:] = (1.0, 0.0, 0.0, 0.8)
            thumb.status_text = ""

    def cleanup(self):
        self.gui_parent = None
        self.controller = None

    def thumb_for_host(self, host):
        def link_host(turn_on):
            self.controller.link(host)

        host_thumb = ui.Thumb(
            "is_linked",
            host,
            setter=link_host,
            label=host.name[:2],
            hotkey=host.name[0],
        )
        # host_thumb.on_color[:] = (1, 0.0, 0.0, 0.8)
        return host_thumb
