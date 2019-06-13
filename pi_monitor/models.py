import abc
import heapq
import logging
import typing as T

import ndsi

from .observable import Observable

logger = logging.getLogger(__name__)


class SortedHostDict(dict):
    def values(self) -> T.List["Host"]:
        return sorted(super().values(), key=lambda host: host.name)


class Host:
    def __init__(self, host_uuid, name):
        self.host_uuid = host_uuid
        self.name = name
        self.sensors = {"gaze": None, "video": None}
        self.is_linked = False

    @property
    def is_connected(self) -> bool:
        return any(self.sensors.values())

    def add_sensor(self, network, sensor_type: str, sensor_uuid: str, sensor_name: str):
        if sensor_type == "video" and "world" not in sensor_name:
            return

        sensor = network.sensor(sensor_uuid)
        sensor.set_control_value("streaming", True)
        sensor.refresh_controls()
        self.sensors[sensor_type] = sensor
        logger.info(f"Attached: {sensor}")

    def remove_sensor(self, sensor_uuid: str):
        for sensor_type, sensor in self.sensors.items():
            if sensor and sensor.uuid == sensor_uuid:
                logger.info(f"Detached: {sensor}")
                sensor.unlink()
                self.sensors[sensor_type] = None

    def fetch_recent_frame(self):
        pass

    def fetch_recent_gaze(self):
        pass

    def link(self):
        pass

    def unlink(self):
        pass

    def cleanup(self):
        for sensor in self.sensors.values():
            if sensor:
                sensor.unlink()
        self.sensors.clear()


class Host_Controller(Observable):
    sensor_types = ("video", "gaze")

    def __init__(self):
        self.hosts = SortedHostDict()
        self.network = ndsi.Network(callbacks=(self.on_event,))
        self.network.start()

    def cleanup(self):
        for host in self.hosts.values():
            host.cleanup()
        self.network.stop()

    def poll_events(self):
        while self.network.has_events:
            self.network.handle_event()

    def on_event(self, caller, event):
        if event["subject"] == "attach" and event["sensor_type"] in self.sensor_types:
            host_uuid = event["host_uuid"]
            if host_uuid not in self.hosts:
                host = Host(host_uuid, event["host_name"])
                self.hosts[host_uuid] = host
                host_idx = self.hosts.values().index(host)
                self.on_host_added(host_idx)

            host = self.hosts[host_uuid]
            host.add_sensor(
                self.network,
                event["sensor_type"],
                event["sensor_uuid"],
                event["sensor_name"],
            )
            host_idx = self.hosts.values().index(host)
            self.on_host_changed(host_idx)

        if event["subject"] == "detach" and event["host_uuid"] in self.hosts:
            host = self.hosts[event["host_uuid"]]
            host_idx = self.hosts.values().index(host)
            host.remove_sensor(event["sensor_uuid"])
            self.on_host_changed(host_idx)
            if not host.is_connected:
                del self.hosts[event["host_uuid"]]
                self.on_host_removed(host_idx)

    def link(self, host):
        logger.info(f"Link {host}")

    def on_host_added(self, host_idx):
        pass

    def on_host_removed(self, host_idx):
        pass

    def on_host_changed(self, host_idx):
        pass
