#!/usr/bin/env python3
# =============================================================================
"""
@brief Code Information:
    Device class
"""
# =============================================================================

from .resource_base import Resource, Foreign, ResourceGroup, ResourceNotFound
from .device_env import DeviceEnv
from .device_service_env import DeviceServiceEnv
from .fleet_env import FleetEnv
from .fleet_service_env import FleetServiceEnv
from .service import ServiceInstall
from typing import List

# =============================================================================


class Device(Resource):

    name = "device"

    @classmethod
    def fromFleet(
        cls,
        fleet_id: int | str,
        select: str | List[str] | None = None,
        expand: str | None = None,
        pagination: int = 100,
        addToGroup: ResourceGroup | None = None,
    ):
        """! Get fleet devices
        @param fleet_id int | str
        @param select str | List[str]
            get only listed fields
        @param expand str
            Expand to foreign resources
        @param pagination
        @param addToGroup
            ResourceGroup instance to add the devices
        @return device Resourcegroup
        """

        if addToGroup is None:
            addToGroup = ResourceGroup(cls)

        addToGroup.include(
            f"belongs_to__application eq {fleet_id}", select, expand, pagination
        )

        return addToGroup

    @classmethod
    def fromDeviceName(
        cls,
        device_name: str,
        select: str | List[str] | None = None,
        expand: str | None = None,
    ):
        """! Get a device from it's device name
        @param device_name str
        @param select str | List[str]
            get only listed fields
        @param expand str
            Expand to foreign resources
        @return new device instance
        """
        return cls.fromField("device_name", device_name, select, expand)

    @classmethod
    def fromUuid(
        cls, uuid: str, select: str | List[str] | None = None, expand: str | None = None
    ):
        """! Get a device from it's device name
        @param device_name str
        @param select str | List[str]
            get only listed fields
        @param expand str
            Expand to foreign resources
        @return new device instance
        """
        return cls.fromField("uuid", uuid, select, expand)

    def __init__(self, id: int | str | None):
        from .fleet import Fleet
        from .device_tag import DeviceTag
        from .release import Release
        from .service import ServiceInstall

        self.fleet = Foreign("belongs_to__application", Fleet)
        self.tags = Foreign("device_tag", DeviceTag, multi=True)
        self.release_running = Foreign("is_running__release", Release)
        self.release_pinned = Foreign("should_be_running__release", Release)
        self.service_install = Foreign("service_install", ServiceInstall, multi=True)
        super().__init__(id)

    def __str__(self):

        return (
            self.data["device_name"]
            if "device_name" in self.data.keys()
            else str(self.id)
        )

    def set_env(self, name: str, value: str, service_name: str | None = None) -> bool:
        """! Update Device variable
            Creates it if it doesn't exist
        @param name: str
        @param value: str
        @param service_name: str | None
            if left to None, update env variables,
        @return bool
            True if Success
        """
        if self.id is None:
            return False
        if service_name is None or service_name == "*":
            try:
                env = DeviceEnv.fromDeviceAndName(self.id, name, select="id")
                env.patch({"value": value})
            except ResourceNotFound:
                # Then create it
                DeviceEnv.new({"device": f"{self.id}", "name": name, "value": value})
        else:
            fleet = self.fleet.get_instances()
            if isinstance(fleet, ResourceGroup) or fleet is None or fleet.id is None:
                return False
            try:
                env = DeviceServiceEnv.fromDeviceAndName(self.id, name, select="id")
                env.patch({"value": value})
            except ResourceNotFound:
                # Then create it
                install = ServiceInstall.fromFilter(
                    f"installs__service/service_name eq '{service_name}' and installs__service/application eq {fleet.id} and device eq {self.id}",
                    select="id",
                )
                DeviceServiceEnv.new(
                    {"service_install": str(install.id), "name": name, "value": value}
                )
        return True

    def overwrite_env(self, name: str, value: str) -> bool:
        """! Overwrites a variable acording to it's fleet definition
            If your services have repeated env names, it's recommended to
            use set_env method to specify the service name
        @param name
        @param value
        @return bool
            True in success
        """
        fleet = self.fleet.get_instances()
        if fleet is None or isinstance(fleet, ResourceGroup) or fleet.id is None:
            return False

        try:
            FleetEnv.fromFleetAndName(fleet.id, name, select="id")
            self.set_env(name, value, None)
        except ResourceNotFound:
            # Try with services
            try:
                env = FleetServiceEnv.fromFleetAndName(
                    fleet.id,
                    name,
                    select="id,service",
                    expand="service($select=service_name,id)",
                )
                service_name = env.get_service()["service_name"]
                return self.set_env(name, value, service_name)
            except ResourceNotFound:
                # Variable not in fleet
                return False

        return True

    def _update(self, data: dict) -> None:
        """! Parse data input into objet attributes
        @param data dict
        """

        self.fleet.update(data)
        self.tags.update(data)
        self.release_pinned.update(data)
        self.release_running.update(data)
        self.service_install.update(data)
        self.data.update(data)

    def get_fleet(self):
        """! Returns device's Fleet"""
        return self.fleet.get_instances()

    def get_tags(self):
        """! Returns device's [DeviceTag]"""
        return self.tags.get_instances()

    def get_release_pinned(self):
        return self.release_pinned.get_instances()

    def get_release_running(self):
        return self.release_running.get_instances()

    def get_service_install(self):
        return self.service_install.get_instances()
