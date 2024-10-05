# =============================================================================
"""
@brief Code Information:
    Service class
"""
# =============================================================================

from .resource_base import Resource, Foreign, ResourceGroup, ResourceNotFound
from ..balena import Balena
from typing import List

# =============================================================================


class Service(Resource):

    name = "service"

    @classmethod
    def fromFleet(
        cls,
        fleet_id: str | int,
        select: str | List[str] | None = None,
        expand: str | None = None,
        pagination: int = 100,
        addToGroup: ResourceGroup | None = None,
    ) -> ResourceGroup:
        """! Get the device tag by key and device id
        @param fleet_id str | int
        @param select str | List[str] | None
        @param expand str | None
        @param pagination int
        @return ResourceGroup
        """

        if addToGroup is None:
            addToGroup = ResourceGroup(cls)

        addToGroup.include(f"application eq '{fleet_id}'", select, expand, pagination)

        return addToGroup

    @classmethod
    def fromFleetAndName(
        cls,
        fleet_id: str | int,
        service_name: str,
        select: str | List[str] | None = None,
        expand: str | None = None,
    ) -> Resource:
        """! Get the device tag by key and device id
        @param fleet_id str | int
        @param service_name str
        @param select str | List[str] | None
        @param expand str | None
        """

        filter = f"application eq '{fleet_id}' and service_name eq '{service_name}'"

        return cls.fromFilter(filter, select, expand)

    def __init__(self, id: str | int | None):
        from .fleet import Fleet

        self.fleet = Foreign("application", Fleet)
        super().__init__(id)

    def __str__(self):

        if "service_name" in self.data:
            return self.data["service_name"]
        return f"{self.id}"

    def _update(self, data: dict) -> None:
        """! Parse data input into objet attributes
        @param data dict
        """

        self.fleet.update(data)
        self.data.update(data)

    def get_device(self):
        return self.fleet.get_instances()

    def get_fleet(self):
        return self.fleet.get_instances()


class ServiceInstall(Resource):

    name = "service_install"

    @classmethod
    def fromDevice(
        cls,
        device_id: str | int,
        select: str | List[str] | None = None,
        expand: str | None = None,
        pagination: int = 100,
        addToGroup: ResourceGroup | None = None,
    ) -> ResourceGroup:
        """! Get the device tag by key and device id
        @param tag_key str
        @param select str | List[str] | None
        @param expand str | None
        @param pagination int
        @return ResourceGroup
        """

        if addToGroup is None:
            addToGroup = ResourceGroup(cls)

        addToGroup.include(f"device eq '{device_id}'", select, expand, pagination)

        return addToGroup

    @classmethod
    def fromDeviceAndFleet(
        cls,
        device_id: str | int,
        fleet_id: str | int,
        select: str | List[str] | None = None,
        expand: str | None = None,
        pagination: int = 100,
        addToGroup: ResourceGroup | None = None,
    ) -> ResourceGroup:
        """! Get the device tag by key and device id
        @param device_id str | int
        @param fleet_id str | int
        @param select str | List[str] | None
        @param expand str | None
        @param pagination int
        @return ResourceGroup
        """

        filter = (
            f"device eq '{device_id}' and installs__service/application eq {fleet_id}"
        )

        if addToGroup is None:
            addToGroup = ResourceGroup(cls)

        addToGroup.include(filter, select, expand, pagination)

        return addToGroup

    @classmethod
    def fromDeviceAndService(
        cls,
        device_id: str | int,
        service_id: str | int,
        select: str | List[str] | None = None,
        expand: str | None = None,
        pagination: int = 100,
        addToGroup: ResourceGroup | None = None,
    ) -> ResourceGroup:
        """! Get the device tag by key and device id
        @param device_id str | int
        @param service_id str | int
        @param select str | List[str] | None
        @param expand str | None
        @param pagination int
        @return ResourceGroup
        """

        filter = f"device eq '{device_id}' and installs__service eq {service_id}"

        if addToGroup is None:
            addToGroup = ResourceGroup(cls)

        addToGroup.include(filter, select, expand, pagination)

        return addToGroup

    def __init__(self, id: str | int | None):
        from .device import Device

        self.service = Foreign("installs__service", Service)
        self.device = Foreign("device", Device)
        super().__init__(id)

    def __str__(self):

        return f"{self.id}"

    def _update(self, data: dict) -> None:
        """! Parse data input into objet attributes
        @param data dict
        """

        self.device.update(data)
        self.service.update(data)
        self.data.update(data)

    def get_device(self):
        return self.device.get_instances()

    def get_service(self):
        return self.service.get_instances()
