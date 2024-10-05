#!/usr/bin/env python3
# =============================================================================
"""
@brief Code Information:
    Device class
"""
# =============================================================================

from .fleet_env import FleetEnv
from .fleet_service_env import FleetServiceEnv
from .service import Service
from .resource_base import Resource, Foreign, ResourceGroup, ResourceNotFound
from typing import List

# =============================================================================


class Fleet(Resource):

    name = "application"

    @classmethod
    def fromUser(
        cls,
        select: str | List[str] | None = None,
        expand: str | None = None,
        pagination: int = 100,
        addToGroup: ResourceGroup | None = None,
    ):
        """! Get fleet devices
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
            "is_directly_accessible_by__user/any(dau:1%20eq%201)",
            select,
            expand,
            pagination,
        )

        return addToGroup

    @classmethod
    def fromAppName(
        cls,
        app_name: str,
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

        return cls.fromField("app_name", app_name, select, expand)

    def __init__(self, id: str | int | None):
        from .release import Release
        from .service import Service

        self.release = Foreign("should_be_running__release", Release)
        self.service = Foreign("service", Service, multi=True)

        super().__init__(id)

    def __str__(self):

        return self.data["app_name"] if "app_name" in self.data.keys() else str(self.id)


    def set_env(self, name: str, value: str, service_name: str | None = "*") -> bool:
        """! Update Fleet variable
            Creates it if it doesn't exist
        @param name: str
        @param value: str
        @param service_name: str | None
            if left to None, update env variables,
        @return bool
            True if Success
        """
        if self.id is None: return False
        if service_name is None or service_name == "*":
            try:
                env = FleetEnv.fromFleetAndName(self.id, name)
                env.patch({"value": value})
            except ResourceNotFound:
                # The variable doesn't exist, then create it
                FleetEnv.new({"application": self.id, "name": name, "value": value})

        else:
            try:
                service = Service.fromFleetAndName(
                        fleet_id=self.id,
                        service_name=service_name)
                if service.id == None:
                    return False # Unexpected error
            except ResourceNotFound:
                return False

            try:
                env = FleetServiceEnv.fromServiceAndName(service_id=service.id, name=name)
                env.parch({"value": value})
            except ResourceNotFound:
                # The variable doesn't exist, then create it
                FleetEnv.new({"service": service.id, "name": name, "value": value})

        return True

    def _update(self, data: dict) -> None:
        """! Parse data input into objet attributes
        @param data dict
        """

        self.release.update(data)
        self.service.update(data)
        self.data.update(data)

    def get_release(self):
        return self.release.get_instances()

    def get_services(self):
        return self.service.get_instances()
