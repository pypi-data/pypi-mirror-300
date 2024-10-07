from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_permission_groups_scope_type import ListPermissionGroupsScopeType
from ...models.permission_group import PermissionGroup
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    scope_type: Union[Unset, None, ListPermissionGroupsScopeType] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    json_scope_type: Union[Unset, None, str] = UNSET
    if not isinstance(scope_type, Unset):
        json_scope_type = scope_type.value if scope_type else None

    params["scopeType"] = json_scope_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/authorization/permission-groups",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, List["PermissionGroup"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = PermissionGroup.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = Error.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = Error.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = Error.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = Error.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, List["PermissionGroup"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    scope_type: Union[Unset, None, ListPermissionGroupsScopeType] = UNSET,
) -> Response[Union[Error, List["PermissionGroup"]]]:
    """List authorization permission groups

     List the available permissions you can grant to a custom role.

    Args:
        scope_type (Union[Unset, None, ListPermissionGroupsScopeType]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, List['PermissionGroup']]]
    """

    kwargs = _get_kwargs(
        scope_type=scope_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    scope_type: Union[Unset, None, ListPermissionGroupsScopeType] = UNSET,
) -> Optional[Union[Error, List["PermissionGroup"]]]:
    """List authorization permission groups

     List the available permissions you can grant to a custom role.

    Args:
        scope_type (Union[Unset, None, ListPermissionGroupsScopeType]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, List['PermissionGroup']]
    """

    return sync_detailed(
        client=client,
        scope_type=scope_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    scope_type: Union[Unset, None, ListPermissionGroupsScopeType] = UNSET,
) -> Response[Union[Error, List["PermissionGroup"]]]:
    """List authorization permission groups

     List the available permissions you can grant to a custom role.

    Args:
        scope_type (Union[Unset, None, ListPermissionGroupsScopeType]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, List['PermissionGroup']]]
    """

    kwargs = _get_kwargs(
        scope_type=scope_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    scope_type: Union[Unset, None, ListPermissionGroupsScopeType] = UNSET,
) -> Optional[Union[Error, List["PermissionGroup"]]]:
    """List authorization permission groups

     List the available permissions you can grant to a custom role.

    Args:
        scope_type (Union[Unset, None, ListPermissionGroupsScopeType]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, List['PermissionGroup']]
    """

    return (
        await asyncio_detailed(
            client=client,
            scope_type=scope_type,
        )
    ).parsed
