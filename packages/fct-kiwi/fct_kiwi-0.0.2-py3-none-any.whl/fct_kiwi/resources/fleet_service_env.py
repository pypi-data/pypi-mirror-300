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


class FleetServiceEnv(Resource):

    name = "service_environment_variable"

    @classmethod
    def fromFleet(
        cls,
        fleet_id: int | str,
        select: str | List[str] | None = None,
        expand: str | None = None,
        pagination: int = 100,
        addToGroup: ResourceGroup | None = None,
    ) -> ResourceGroup:
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
            f"service/application eq {fleet_id}", select, expand, pagination
        )

        return addToGroup

    @classmethod
    def fromFleetAndName(
        cls,
        fleet_id: str | int,
        name: str,
        select: str | List[str] | None = None,
        expand: str | None = None,
    ):
        """! Get a device from it's device name
        @param fleet_id str | int
        @param name str
        @param select str | List[str]
            get only listed fields
        @param expand str
            Expand to foreign resources
        @return new device instance
        """
        filter = f"service/application eq {fleet_id} and name eq '{name}'"

        return cls.fromFilter(filter, select, expand)

    @classmethod
    def fromServiceAndName(
        cls,
        service_id: str | int,
        name: str,
        select: str | List[str] | None = None,
        expand: str | None = None,
    ):
        """! Get a variable from service id and name
        @param service_id str | int
        @param name str
        @param select str | List[str]
            get only listed fields
        @param expand str
            Expand to foreign resources
        @return new device instance
        """
        filter = f"service eq {service_id} and name eq '{name}'"

        return cls.fromFilter(filter, select, expand)

    def __init__(self, id: int | str | None):
        from .service import Service

        self.service = Foreign("service", Service)
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

        self.service.update(data)
        self.data.update(data)

    def get_service(self):
        return self.service.get_instances()
