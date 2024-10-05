#!/usr/bin/env python3
# =============================================================================
"""
@brief Code Information:
    Maps requests to Balena API
"""
# =============================================================================

from requests import get, patch, post, delete, Response
from os import getenv
from .configs.settings import Settings

# =============================================================================


def check_requests_response(function):
    """! Decorator for functions that return a requests.Response object to
    check if the request was successful and raise an exception if not.
    @param function callable
        Function that returns a requests.Response object.
    @return callable
        The same function checked if the request was successful.
    """

    def wrapper(*args, **kwargs):
        response = function(*args, **kwargs)
        if isinstance(response, Response):
            response.raise_for_status()
        return response

    return wrapper


def uri_element_replace(uri_element: str | list) -> str:
    """! Replace spaces with '%20' in URI elements and join list elements with commas.
    @param uri_element str or list
        The URI element to be processed.
    @return str
        The processed URI element.
    """

    if isinstance(uri_element, list):
        out = ",".join(uri_element)
    else:
        out = str(uri_element)

    out = out.replace(" ", "%20")
    return out


def uri_wrap(resource: str, resource_id: str | list = "", **params) -> str:
    """! Wrap URI elements into a complete URL with query parameters.
    @param resource str
        The API resource to be accessed.
    @param resource_id str or list, optional
        The identifier for the resource, by default "".
    @param params dict
        Additional query parameters.
    @return str
        The complete URL.
    """

    fixed_params = [
        f"${key}={uri_element_replace(value)}" for key, value in params.items()
    ]
    fixed_params = "&".join(fixed_params)
    if resource_id:
        url = f"{Settings.balena_api_url}{resource}({resource_id})"
    else:
        url = f"{Settings.balena_api_url}{resource}"
    return "?".join([url, fixed_params])


class Balena:
    """!Manage balena API requests"""

    balena_api_key: str | None = getenv(Settings.balena_api_key_env_name)
    authenticated = balena_api_key is not None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {balena_api_key}",
    }

    @classmethod
    def is_authenticated(cls) -> bool:
        """! Return True if a balena API key was provided.
        @return bool
            True if authenticated, False otherwise.
        """
        return cls.authenticated

    @classmethod
    def authenticate(cls, balena_api_key: str | None):
        """! Authenticate with the given balena API key.
        @param balena_api_key str or None
            The balena API key for authentication.
        """
        cls.balena_api_key = balena_api_key
        cls.authenticated = balena_api_key is not None

        if cls.authenticated:
            cls.headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {cls.balena_api_key}",
            }

    @classmethod
    @check_requests_response
    def api_get(cls, resource: str, resource_id: str | int = "", **params) -> Response:
        """! Make a GET request to balena API.
        @param resource str
            Balena API resource to request.
        @param resource_id str or int, optional
            Resource identifier, by default "".
        @param params dict
            OData system query options.
        @return Response
            requests.Response object.
        @example
        @code
        >>> response = Balena.api_get("device",
        ...                           filter="is_online",
        ...                           select="device_name,id",
        ...                           orderby="device_name asc")
        >>> if response.status_code >= 300:
        ...     print("%s: %s" % (response.status_code, response.reason))
        ...     exit(1)
        >>> response.json()["d"][0]
        {'device_name': 'kiwibot4B105', 'id': 5751...}
        @endcode
        """

        url = uri_wrap(resource, str(resource_id), **params)
        return get(url, headers=cls.headers)

    @classmethod
    @check_requests_response
    def api_post(cls, resource: str, data: dict, **params) -> Response:
        """! Make a POST request to balena API.
        @param resource str
            Balena API resource to request.
        @param data dict
            HTTP POST data.
        @param params dict
            OData system query options.
        @return Response
            requests.Response object.
        """

        url = uri_wrap(resource, **params)
        return post(url, headers=cls.headers, json=data)

    @classmethod
    @check_requests_response
    def api_delete(
        cls, resource: str, resource_id: str | int = "", force: bool = False, **params
    ) -> Response:
        """! Make a DELETE request to balena API.
        @param resource str
            Balena API resource to request.
        @param resource_id str or int, optional
            Resource identifier, by default "".
        @param force bool
            False by default, prevents deleting protected
            resources
        @param params dict
            OData system query options.
        @return Response
            requests.Response object.
        @throws ValueError
            If the resource is protected: 'device' or 'application'
            by default, to delete a protected resource use force=True.
        """

        if not force and resource in Settings.protected_resources:
            raise ValueError(
                f"Using api_delete with '{resource}' resource is protected"
            )
        url = uri_wrap(resource, str(resource_id), **params)
        return delete(url, headers=cls.headers)

    @classmethod
    @check_requests_response
    def api_patch(
        cls, resource: str, resource_id: str | int, data: dict, **params
    ) -> Response:
        """! Make a PATCH request to balena API.
        @param resource str
            Balena API resource to request.
        @param resource_id str or int
            Resource identifier.
        @param data dict
            HTTP PATCH data.
        @param params dict
            OData system query options.
        @return Response
            requests.Response object.
        """

        url = uri_wrap(resource, str(resource_id), **params)
        return patch(url, headers=cls.headers, json=data)
    
    @classmethod
    @check_requests_response
    def get_device_logs(cls, uuid: str, count: int = 1000) -> Response:
        """! Get latest count available logs
        @param uuid str
            Device uuid
        @param count int
            Number of logs to receive
        @return Response
            requests.Response object
        """
        url = f"https://api.balena-cloud.com/device/v2/{uuid}/logs?count={count}"
        return get(url, headers=cls.headers)
