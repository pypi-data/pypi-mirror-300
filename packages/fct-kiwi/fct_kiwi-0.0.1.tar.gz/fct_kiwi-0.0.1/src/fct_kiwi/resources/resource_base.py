#!/usr/bin/env python3
# =============================================================================
"""
@brief Code Information:
    Resource base class
"""
# =============================================================================

from ..balena import Balena
from typing import List, Type
from requests.exceptions import HTTPError

# =============================================================================


class ResourceNotFound(Exception):
    """! Raised when resource was not found"""

    pass


class UnnamedResourceException(Exception):
    """! Raised when resource name is not defined"""

    pass


class EmptyResourceException(Exception):
    """! Raised when resource id is required but not specified"""

    pass


class Resource:
    """! Base abstraction of a balena resource"""

    name = None

    registry = None

    @classmethod
    def register(cls, resource):
        """! Register a resource into Resource.registry
        @param resource: Type[Resource]
        """

        if cls.registry is None:
            cls.registry = ResourceGroup(cls)

        return cls.registry.append(resource)

    @classmethod
    def get_registry(cls):
        return cls.registry

    @classmethod
    def new(cls, data: dict) -> int:
        """! Tries to create a new resource in balena cloud
        @param data dict
        @return Request status code
        """

        if cls.name is None:
            raise UnnamedResourceException("Cant create an unnamed resource")

        try:
            response = Balena.api_post(cls.name, data)
        except HTTPError as e:
            # Return silently
            return e.response.status_code

        return response.status_code

    @classmethod
    def fromData(cls, data: dict):
        """! Load a resource from a data dictionary
        @param data dict
            data dictionary (Must include resource id)
        @return Resource
            resource instance
        """

        if not "id" in data:
            raise EmptyResourceException(
                "Can't create resource if id is not provided in the data dict"
            )

        new_resource = cls(data["id"])
        new_resource._update(data)

        return cls.register(new_resource)

    @classmethod
    def fromFilter(
        cls,
        filter: str,
        select: str | List[str] | None = None,
        expand: str | None = None,
    ):
        """! Get a device from it's device name
        @param field_name str
        @param field_value str
        @param select str | List[str]
            get only listed fields
        @param expand str
            Expand to foreign resources
        @return new device instance
        """

        kwargs = {"resource": cls.name, "filter": filter}
        if select is not None:
            if isinstance(select, list):
                select = ",".join(select)
            if not "id" in select:
                if isinstance(select, list):
                    select.append("id")
                else:
                    select += ",id"
            kwargs["select"] = select
        if expand is not None:
            kwargs["expand"] = expand

        response = Balena.api_get(**kwargs)
        response_data = response.json()["d"]
        if len(response_data) < 1:
            raise ResourceNotFound()

        return cls.fromData(response_data[0])

    @classmethod
    def fromField(
        cls,
        field_name: str,
        field_value: str,
        select: str | List[str] | None = None,
        expand: str | None = None,
    ):
        """! Get a device from it's device name
        @param field_name str
        @param field_value str
        @param select str | List[str]
            get only listed fields
        @param expand str
            Expand to foreign resources
        @return new device instance
        """

        filter = f"{field_name} eq '{field_value}'"

        return cls.fromFilter(filter, select, expand)

    def __init__(self, id: int | str | None):

        self.data: dict = {}
        self.id: int | str | None = id
        self.groups = []

    def raise_for_configuration(self) -> None:
        """! Raises an EmptyResourceException if object id
        and UnnamedResourceException if Resource name is None
        """

        if self.id is None:
            raise EmptyResourceException("Tried to update an empty resource")

        if self.__class__.name is None:
            raise UnnamedResourceException(
                f"{self.__class__.__name__}.name is None,"
                + " it must name a balena resource"
            )

        return

    def clear(self):
        """! Clears resource data"""
        self.data = {}

    def patch(self, data: dict) -> int:
        """! Patch resource
        @param data dict
            new resource data
        @return int
            Request status code
        """

        self.raise_for_configuration()

        try:
            response = Balena.api_patch(str(self.__class__.name), str(self.id), data)
        except HTTPError as e:
            # Return silently
            return e.response.status_code

        self._update(data)
        return response.status_code

    def delete(self, force: bool = False) -> int:
        """! Deletes the current resource from balena Cloud
        @param force bool
            set to true to delete protected resources
        @response int
            Request status code
        """

        self.raise_for_configuration()

        try:
            response = Balena.api_delete(str(self.__class__.name), str(self.id), force)
        except HTTPError as e:
            # Return silently
            return e.response.status_code

        for group in self.groups:
            group.pop(self.id)

        return response.status_code

    def update(
        self, select: List[str] | str | None = None, expand: str | None = None
    ) -> int:
        """! Fetch balena API to update resource data
        @param select List[str] | int
            Select resource fields to update
        @param expand str
            Expand a field corresponding to a resource to include
            the foreign resource fields in the response
        @return int
            request status code
        """

        self.raise_for_configuration()

        request_kwargs = {"resource": self.__class__.name, "resource_id": self.id}
        if select is not None:
            request_kwargs["select"] = select
        if expand is not None:
            request_kwargs["expand"] = expand

        try:
            response = Balena.api_get(**request_kwargs)
        except HTTPError as e:
            # Return status code silently
            return e.response.status_code

        self._update(response.json()["d"][0])

        return response.status_code

    def _update(self, data: dict) -> None:
        """! Virtual method to parse a dictionary to update
            the device current data
        @param data dict
            new data to update
        """
        self.data.update(data)

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def __getitem__(self, keys):
        """! [] Operator overload"""
        return self.data.__getitem__(keys)

    def __setitem__(self, keys, value):
        """! [] Operator overload"""
        return self.data.__setitem__(keys, value)


class Foreign:
    """! Foreign class holding expanded resources"""

    def __init__(
        self, resource_key: str, resource_type: Type[Resource], multi: bool = False
    ):
        """!
        @param resource_key str
            The field name given to the foreign resource in balena, usually
            they have a double underscore '__' before the resource name
        @param resource_type Type[Resource]
            Resource inherited class name
        @param multi bool
            Set for Foreign resources that hold more than one resource
            example: device/device_tags
        """

        self.key = resource_key
        self.cls = resource_type
        self.multi = multi
        self.instance = None

    def update(self, data: dict):
        """! Update the foreign resource
        @param data list
            list of resource returned by Balena API when `expand`
            option is used
        """

        if self.multi:
            self._update_multi(data)
        else:
            self._update_single(data)

    def _update_single(self, parent_data: dict):
        """! Update a Foreign resourc which can only return a single resource
        @param data list
        """

        if not self.key in parent_data.keys():
            return

        data = parent_data[self.key]

        if isinstance(data, dict):
            update_data = {"id": data["__id"]}
        elif isinstance(data, list):
            update_data = data[0]
        else:
            return

        if self.instance is None and "id" in update_data.keys():
            self.instance = self.cls.fromData(update_data)
        elif isinstance(self.instance, Resource):
            self.instance._update(update_data)

    def _update_multi(self, parent_data: dict):
        """! Update a Foreign resourc which can only return a single resource
        @param data dict
        """

        if not self.key in parent_data.keys():
            return

        data = parent_data[self.key]

        if self.instance is None:
            self.instance = ResourceGroup(self.cls)

            for resource_data in data:
                new_resource = self.cls.fromData(resource_data)
                self.instance.append(new_resource)

        elif isinstance(self.instance, ResourceGroup):
            updated_resources = []
            for resource in data:
                if not "id" in resource.keys():
                    break
                # Update resources
                if resource["id"] in self.instance.keys():
                    self.instance[resource["id"]]._update(resource)

                    updated_resources.append(resource["id"])
                else:
                    new_resource = self.cls.fromData(resource)

                    self.instance.append(new_resource)
                    updated_resources.append(resource["id"])

            for id in self.instance.keys():
                if not id in updated_resources:
                    # Resource was removed in balena, thus here as well
                    self.instance.pop(id)

    def get_instances(self):
        """! Returns Foreign resources
        @return ResourceGroup | Resource | None
            returns a ResourceGroup when multi is set to True
            and None when the resource is empty (no expanded request
            has been made)
        """

        return self.instance


class ResourceGroup:
    def __init__(self, resource_type: Type[Resource]):

        self.lookup = {}
        self.filter = None
        self.lone_ids = []
        self.cls = resource_type

    def include(
        self,
        filter: str,
        select: str | List[str] | None = None,
        expand: str | None = None,
        pagination: int = 100,
    ) -> None:
        """! Adds new resources to the group returned by the filter
        @param filer str
            New filter to add
        @param select str
            select only the fields
        @param expand str
        """

        if self.cls.name is None:
            return

        if self.filter is None or self.filter == "()":
            self.filter = f"({filter})"
        else:
            self.filter += f" or ({filter})"

        self.update(select, expand, pagination)

    def pop(self, resource_id: int | str):
        """! Pops a resource from the lookup table
        @param resource_id int | str
        """

        if resource_id in self.lookup.keys():
            del self.lookup[resource_id]

    def get_filter(self) -> str | None:
        """! Construct the filter including lone devices"""

        if self.lone_ids != []:
            if self.filter is not None and self.filter != "()":
                filt = self.filter + " or id in ("
            else:
                filt = "id in ("
            for i in range(len(self.lone_ids)):
                if i > 0:
                    filt += ","
                filt += f"'{self.lone_ids[i]}'"
            filt += ")"
            return filt
        else:
            return self.filter

    def append(self, resource: Resource):
        """! Add new resource to the group (if the number of resources will
            be large, it is recommended to use addFilter)
        @param resource Resource
            Resource to append
        @return Type[Resource]
            Resource saved in the registry
        """

        if resource.id in self.lookup.keys():
            self.lookup[resource.id]._update(resource.data)
            return self.lookup[resource.id]

        resource.groups.append(self)
        self.lookup[resource.id] = resource

        self.lone_ids.append(resource.id)

        return self.lookup[resource.id]

    def update_each(
        self, select: List[str] | str | None = None, expand: str | None = None
    ):
        """! Update resources making a request for each
        @param select
        @param expand
        """

        for resource in self.lookup.values():
            resource.update(select, expand)

    def update(
        self,
        select: List[str] | str | None = None,
        expand: str | None = None,
        pagination: int = 100,
    ):
        """! Update all the resources in a paginated api request using filters
        @param select
        @param expand
        @param pagination
            The maximum number of resources returned by request,
            this helps balena Cloud deal with less data per request,
            enhancing the health of the operation.
        """

        if self.filter is None and self.lone_ids == []:
            return self.update_each(select, expand)

        kwargs = {
            "resource": self.cls.name,
            "top": pagination,
        }

        filt = self.get_filter()
        if self.filter != "()":
            kwargs["filter"] = filt

        if expand is not None:
            kwargs["expand"] = expand

        if select is not None:
            if not "id" in select:
                if isinstance(select, list):
                    select.append("id")
                else:
                    select += ",id"
            kwargs["select"] = select

        response_data = []
        page = 0
        last_response = []

        while len(last_response) == pagination or page == 0:
            kwargs["skip"] = page

            last_response = Balena.api_get(**kwargs).json()["d"]

            response_data += last_response
            page += pagination

        for resource in response_data:
            if not resource["id"] in self.lookup.keys():
                new_resource = self.cls(resource["id"])
                new_resource.groups.append(self)
                self.lookup[resource["id"]] = self.cls.register(new_resource)
            self.lookup[resource["id"]]._update(resource)

    def patch(self, data: dict):
        """! Patch all resources in group
        @param data dict
            new resource data
        @return int
            Request status code
        """

        for resource in self.lookup.values():
            resource.patch(data)

    def delete(self, force: bool = False):
        """! Deletes all resources in group
        @param force bool
            set to true to delete protected resources
        @response int
            Request status code
        """

        for resource in self.lookup.values():
            resource.delete(force)

    def clear(self):
        """! Clears data of the grouped resources"""
        for resource in self.lookup.values():
            resource.clear()

    def keys(self):
        """! Get a list of the resources"""
        return self.lookup.keys()

    def values(self):
        """! Get a list of the resources"""
        return self.lookup.values()

    def __getitem__(self, keys):
        """! [] Operator overload"""
        return self.lookup.__getitem__(keys)

    def __str__(self):
        s = f"<ResourceGroup[{self.cls.__name__}]>: ["
        for resource in self.lookup.values():
            s += str(resource) + ", "
        s += "\b\b]"
        return s
