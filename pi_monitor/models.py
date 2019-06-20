import logging
import typing as T

import ndsi

from .observable import Observable

logger = logging.getLogger(__name__)


class SortedHostDict(dict):
    def sorted_values(self) -> T.List["Host"]:
        return sorted(super().values(), key=lambda host: host.name)


class Host:
    def __init__(self, host_uuid, name):
        self.host_uuid = host_uuid
        self.name = name
        self.sensor_uuids = {}
        self.sensors = {}
        self.is_linked = False
        self.is_in_bad_state = False

    def __str__(self):
        return f"<{type(self).__name__} {self.name}>"

    @property
    def is_connected(self) -> bool:
        return any(self.sensors.values())

    @property
    def is_available(self) -> bool:
        return any(self.sensor_uuids.values())

    def add_sensor(self, network, sensor_type: str, sensor_uuid: str, sensor_name: str):
        if sensor_type == "video" and "world" not in sensor_name:
            return

        logger.debug(f"{self}.add_sensor({sensor_type})")
        self.sensor_uuids[sensor_type] = sensor_uuid

        if self.is_linked:
            self._connect_sensor(network, sensor_type)

    def remove_sensor(self, sensor_uuid_to_removed: str):
        logger.debug(f"{self}.remove_sensor({sensor_uuid_to_removed})")
        for sensor_type, sensor_uuid in self.sensor_uuids.copy().items():
            if sensor_uuid == sensor_uuid_to_removed:
                self._disconnect_sensor(sensor_type)
                del self.sensor_uuids[sensor_type]
                logger.debug(f"Detached: {sensor_type}")

    def poll_notifications(self):
        for sensor in self.sensors.values():
            while sensor.has_notifications:
                sensor.handle_notification()

    def fetch_recent_frame(self):
        if "video" in self.sensors:
            video_sensor = self.sensors["video"]
            try:
                frame = video_sensor.get_newest_data_frame(timeout=0)
            except ndsi.StreamError:
                return
            return frame

    def fetch_recent_gaze(self):
        if "gaze" in self.sensors:
            gaze_sensor = self.sensors["gaze"]
            recent_gaze = None
            for x, y, ts in gaze_sensor.fetch_data():
                recent_gaze = x, y
            return recent_gaze

    def link(self, network):
        logger.debug(f"{self}.link()")
        self.is_linked = True
        for sensor_type in self.sensor_uuids:
            self._connect_sensor(network, sensor_type)

    def _connect_sensor(self, network, sensor_type):
        logger.debug(f"{self}._connect_sensor({sensor_type})")
        sensor_uuid = self.sensor_uuids[sensor_type]

        sensor = network.sensor(sensor_uuid)
        sensor.set_control_value("streaming", True)
        sensor.refresh_controls()
        self.sensors[sensor_type] = sensor

    def unlink(self):
        logger.debug(f"{self}.unlink()")
        for sensor_type in self.sensors.copy():
            self._disconnect_sensor(sensor_type)
        self.is_linked = False

    def _disconnect_sensor(self, sensor_type):
        logger.debug(f"{self}._disconnect_sensor({sensor_type})")
        try:
            sensor = self.sensors[sensor_type]
        except KeyError:
            return
        if sensor:
            sensor.unlink()
        del self.sensors[sensor_type]

    def cleanup(self):
        self.unlink()
        self.sensors.clear()


class Host_Controller(Observable):
    sensor_types = ("video", "gaze")

    def __init__(self):
        logger.info(f"Using NDSI protocol v{ndsi.__protocol_version__}")
        self._hosts = SortedHostDict()
        self.network = ndsi.Network(callbacks=(self.on_event,))
        self.network.start()

    def __getitem__(self, idx: int):
        return self._hosts.sorted_values()[idx]

    def hosts(self):
        yield from self._hosts.sorted_values()

    def index(self, item: Host):
        return self._hosts.sorted_values().index(item)

    def cleanup(self):
        for host in self.hosts():
            host.cleanup()
        self.network.stop()

    def poll_events(self):
        while self.network.has_events:
            self.network.handle_event()

    def on_event(self, caller, event):
        if event["subject"] == "attach" and event["sensor_type"] in self.sensor_types:
            host_uuid = event["host_uuid"]
            if host_uuid not in self._hosts:
                host = Host(host_uuid, event["host_name"])
                self._hosts[host_uuid] = host
                host_idx = self.index(host)
                self.on_host_added(host_idx)

            host = self._hosts[host_uuid]
            host.add_sensor(
                self.network,
                event["sensor_type"],
                event["sensor_uuid"],
                event["sensor_name"],
            )
            host_idx = self.index(host)
            self.on_host_changed(host_idx)

        if event["subject"] == "detach" and event["host_uuid"] in self._hosts:
            host = self._hosts[event["host_uuid"]]
            host_idx = self.index(host)
            host.remove_sensor(event["sensor_uuid"])
            self.on_host_changed(host_idx)
            if not host.is_linked and not host.is_available:
                self.remove_host(event["host_uuid"])

    def link(self, host_to_connect_sensor):
        logger.debug(f"{type(self).__name__}.link({host_to_connect_sensor})")
        for host_idx, host in enumerate(self.hosts()):
            if host is host_to_connect_sensor and not host.is_linked:
                host.link(self.network)
                self.on_host_changed(host_idx)
                self.on_host_linked()
            elif host is not host_to_connect_sensor and host.is_linked:
                host.unlink()
                self.on_host_changed(host_idx)

        for host in self.hosts():
            if not host.is_linked and not host.is_available:
                self.remove_host(host.host_uuid)

    def remove_host(self, host_uuid):
        logger.debug(f"{type(self).__name__}.remove_host({host_uuid})")
        host = self._hosts[host_uuid]
        host_idx = self.index(host)
        del self._hosts[host_uuid]
        self.on_host_removed(host_idx)

    def fetch_recent_data(self):
        for idx, host in enumerate(self.hosts()):
            if host.is_linked:
                host.poll_notifications()
                try:
                    frame = host.fetch_recent_frame()
                    if frame is not None:
                        self.on_recent_frame(frame)

                    gaze = host.fetch_recent_gaze()
                    if gaze:
                        self.on_recent_gaze(gaze)
                except ndsi.sensor.NotDataSubSupportedError:
                    self.is_in_bad_state = True
                    self.on_host_changed(idx)

    def on_host_added(self, host_idx):
        pass

    def on_host_removed(self, host_idx):
        pass

    def on_host_changed(self, host_idx):
        pass

    def on_recent_frame(self, frame):
        pass

    def on_recent_gaze(self, gaze):
        pass

    def on_host_linked(self):
        pass
