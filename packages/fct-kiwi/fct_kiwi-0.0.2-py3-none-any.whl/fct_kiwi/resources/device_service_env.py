#!/usr/bin/env python3
# =============================================================================
"""
@brief Code Information:
    Envs
"""
# =============================================================================

from .resource_base import Resource, Foreign, ResourceGroup
from typing import List

# =============================================================================


class DeviceServiceEnv(Resource):

    name = "device_service_environment_variable"

    @classmethod
    def fromDevice(
        cls,
        device_id: int | str,
        select: str | List[str] | None = None,
        expand: str | None = None,
        pagination: int = 100,
        addToGroup: ResourceGroup | None = None,
    ) -> ResourceGroup:
        """! Get fleet devices
        @param device_id int | str
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
            f"service_install/device eq {device_id}", select, expand, pagination
        )

        return addToGroup

    @classmethod
    def fromDeviceAndName(
        cls,
        device_id: str | int,
        name: str,
        select: str | List[str] | None = None,
        expand: str | None = None,
    ) -> Resource:
        """! Get a device from it's device name
        @param device_id str | int
        @param name str
        @param select str | List[str]
            get only listed fields
        @param expand str
            Expand to foreign resources
        @return new device instance
        """
        filter = f"service_install/device eq {device_id} and name eq '{name}'"

        return cls.fromFilter(filter, select, expand)

    def __init__(self, id: int | str | None):
        from .service import ServiceInstall

        self.service_install = Foreign("service_install", ServiceInstall)
        super().__init__(id)

    def __str__(self):

        if "name" in self.data:
            name = self.data["name"]
        else:
            name = None
        if "value" in self.data:
            value = self.data["value"]
        else:
            value = None

        if name is not None or value is not None:
            return f"{name} : {value}"
        else:
            return str(self.id)

    def _update(self, data: dict) -> None:
        """! Parse data input into objet attributes
        @param data dict
        """

        self.service_install.update(data)
        self.data.update(data)

    def get_service_install(self):
        return self.service_install.get_instances()
