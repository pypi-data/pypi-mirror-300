#!/usr/bin/env python3
# =============================================================================
"""
@brief Code Information:
    Release class
"""
# =============================================================================

from .resource_base import Resource, Foreign, ResourceNotFound
from ..balena import Balena
from typing import List

# =============================================================================


class Release(Resource):

    name = "release"

    @classmethod
    def fromCommit(
        cls,
        commit: str,
        select: str | List[str] | None = None,
        expand: str | None = None,
    ):
        """! Get a release from it's commit
        @param commit str
        @param select str | List[str]
            get only listed fields
        @param expand str
            Expand to foreign resources
        @return new device instance
        """

        return cls.fromField("commit", commit, select, expand)

    @classmethod
    def fromRevision(
        cls,
        revision: str,
        select: str | List[str] | None = None,
        expand: str | None = None,
    ):
        """! Get a release from it's revision
        @param revision str
        @param select str | List[str]
            get only listed fields
        @param expand str
            Expand to foreign resources
        @return new device instance
        """

        return cls.fromField("revision", revision, select, expand)

    @classmethod
    def fromFleetLatest(
        cls,
        app_id: int | str,
        select: str | List[str] | None = None,
        expand: str | None = None,
    ):
        """! Get a a fleet's lattest succesful release
        @param commit str
        @param select str | List[str]
            get only listed fields
        @param expand str
            Expand to foreign resources
        @return new device instance
        """

        kwargs = {
            "resource": cls.name,
            "filter": f"belongs_to__application eq '{app_id}' and status eq 'success'",
            "orderby": "created_at",
            "top": "1",
        }
        if select is not None:
            if isinstance(select, list):
                select = ",".join(select)
            kwargs["select"] = select
        if expand is not None:
            kwargs["expand"] = expand

        response = Balena.api_get(**kwargs)
        response_data = response.json()["d"]
        if len(response_data) < 1:
            raise ResourceNotFound

        return cls.fromData(response_data[0])

    def __init__(self, id: int | str | None):
        from .fleet import Fleet

        self.fleet = Foreign("belongs_to__application", Fleet)

        super().__init__(id)

    def __str__(self):

        return (
            str(self.data["revision"])
            if "revision" in self.data.keys()
            else str(self.id)
        )

    def _update(self, data: dict) -> None:
        """! Parse data input into objet attributes
        @param data dict
        """

        self.fleet.update(data)
        self.data.update(data)

    def get_fleet(self):
        return self.fleet.get_instances()
