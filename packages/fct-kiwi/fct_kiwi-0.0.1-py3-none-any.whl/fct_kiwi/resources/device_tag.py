#!/usr/bin/env python3
# =============================================================================
"""
@brief Code Information:
    Device class
"""
# =============================================================================

from .resource_base import Resource, Foreign, ResourceGroup
from typing import List

# =============================================================================


class DeviceTag(Resource):

    name = "device_tag"

    @classmethod
    def fromKey(
        cls,
        tag_key: str,
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

        addToGroup.include(f"tag_key eq '{tag_key}'", select, expand, pagination)

        return addToGroup

    @classmethod
    def fromKeyAndValue(
        cls,
        tag_key: str,
        value: str,
        exact_value_match: bool = False,
        select: str | List[str] | None = None,
        expand: str | None = None,
        pagination: int = 100,
        addToGroup: ResourceGroup | None = None,
    ) -> ResourceGroup:
        """! Get the device tag by key and device id
        @param tag_key str
        @param value str
        @param contains_values bool
            if True, returns device_tag resouces which passe value
            parameter is a substring of the actual tag value
        @param select str | List[str] | None
        @param expand str | None
        @param pagination int
        @return ResourceGroup
        """

        filter = f"tag_key eq '{tag_key}' and "
        if not exact_value_match:
            filter += f"contains(value,'{value}')"
        else:
            filter += f"value eq '{value}'"

        if addToGroup is None:
            addToGroup = ResourceGroup(cls)

        addToGroup.include(filter, select, expand, pagination)

        return addToGroup

    def __init__(self, id: str | int | None):
        from .device import Device

        self.device = Foreign("device", Device)
        super().__init__(id)

    def __str__(self):
        tag_key = self.data["tag_key"] if "tag_key" in self.data else None
        value = self.data["value"] if "value" in self.data else None

        if tag_key is None and value is None:
            return str(self.id)
        else:
            return f"{tag_key}: {value}"

    def _update(self, data: dict) -> None:
        """! Parse data input into objet attributes
        @param data dict
        """

        self.device.update(data)
        self.data.update(data)

    def get_device(self):
        return self.device.get_instances()
