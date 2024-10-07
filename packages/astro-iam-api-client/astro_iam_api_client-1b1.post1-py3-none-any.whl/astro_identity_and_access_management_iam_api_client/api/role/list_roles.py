from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_roles_scope_types_item import ListRolesScopeTypesItem
from ...models.list_roles_sorts_item import ListRolesSortsItem
from ...models.roles_paginated import RolesPaginated
from ...types import UNSET, Response, Unset


def _get_kwargs(
    organization_id: str,
    *,
    include_default_roles: Union[Unset, None, bool] = UNSET,
    scope_types: Union[Unset, None, List[ListRolesScopeTypesItem]] = UNSET,
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 20,
    sorts: Union[Unset, None, List[ListRolesSortsItem]] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["includeDefaultRoles"] = include_default_roles

    json_scope_types: Union[Unset, None, List[str]] = UNSET
    if not isinstance(scope_types, Unset):
        if scope_types is None:
            json_scope_types = None
        else:
            json_scope_types = []
            for scope_types_item_data in scope_types:
                scope_types_item = scope_types_item_data.value

                json_scope_types.append(scope_types_item)

    params["scopeTypes"] = json_scope_types

    params["offset"] = offset

    params["limit"] = limit

    json_sorts: Union[Unset, None, List[str]] = UNSET
    if not isinstance(sorts, Unset):
        if sorts is None:
            json_sorts = None
        else:
            json_sorts = []
            for sorts_item_data in sorts:
                sorts_item = sorts_item_data.value

                json_sorts.append(sorts_item)

    params["sorts"] = json_sorts

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/organizations/{organizationId}/roles".format(
            organizationId=organization_id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, RolesPaginated]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RolesPaginated.from_dict(response.json())

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
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = Error.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = Error.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, RolesPaginated]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    organization_id: str,
    *,
    client: AuthenticatedClient,
    include_default_roles: Union[Unset, None, bool] = UNSET,
    scope_types: Union[Unset, None, List[ListRolesScopeTypesItem]] = UNSET,
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 20,
    sorts: Union[Unset, None, List[ListRolesSortsItem]] = UNSET,
) -> Response[Union[Error, RolesPaginated]]:
    """List roles

     List available user roles in an Organization.

    Args:
        organization_id (str):
        include_default_roles (Union[Unset, None, bool]):
        scope_types (Union[Unset, None, List[ListRolesScopeTypesItem]]):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 20.
        sorts (Union[Unset, None, List[ListRolesSortsItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RolesPaginated]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        include_default_roles=include_default_roles,
        scope_types=scope_types,
        offset=offset,
        limit=limit,
        sorts=sorts,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_id: str,
    *,
    client: AuthenticatedClient,
    include_default_roles: Union[Unset, None, bool] = UNSET,
    scope_types: Union[Unset, None, List[ListRolesScopeTypesItem]] = UNSET,
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 20,
    sorts: Union[Unset, None, List[ListRolesSortsItem]] = UNSET,
) -> Optional[Union[Error, RolesPaginated]]:
    """List roles

     List available user roles in an Organization.

    Args:
        organization_id (str):
        include_default_roles (Union[Unset, None, bool]):
        scope_types (Union[Unset, None, List[ListRolesScopeTypesItem]]):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 20.
        sorts (Union[Unset, None, List[ListRolesSortsItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RolesPaginated]
    """

    return sync_detailed(
        organization_id=organization_id,
        client=client,
        include_default_roles=include_default_roles,
        scope_types=scope_types,
        offset=offset,
        limit=limit,
        sorts=sorts,
    ).parsed


async def asyncio_detailed(
    organization_id: str,
    *,
    client: AuthenticatedClient,
    include_default_roles: Union[Unset, None, bool] = UNSET,
    scope_types: Union[Unset, None, List[ListRolesScopeTypesItem]] = UNSET,
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 20,
    sorts: Union[Unset, None, List[ListRolesSortsItem]] = UNSET,
) -> Response[Union[Error, RolesPaginated]]:
    """List roles

     List available user roles in an Organization.

    Args:
        organization_id (str):
        include_default_roles (Union[Unset, None, bool]):
        scope_types (Union[Unset, None, List[ListRolesScopeTypesItem]]):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 20.
        sorts (Union[Unset, None, List[ListRolesSortsItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RolesPaginated]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        include_default_roles=include_default_roles,
        scope_types=scope_types,
        offset=offset,
        limit=limit,
        sorts=sorts,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_id: str,
    *,
    client: AuthenticatedClient,
    include_default_roles: Union[Unset, None, bool] = UNSET,
    scope_types: Union[Unset, None, List[ListRolesScopeTypesItem]] = UNSET,
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 20,
    sorts: Union[Unset, None, List[ListRolesSortsItem]] = UNSET,
) -> Optional[Union[Error, RolesPaginated]]:
    """List roles

     List available user roles in an Organization.

    Args:
        organization_id (str):
        include_default_roles (Union[Unset, None, bool]):
        scope_types (Union[Unset, None, List[ListRolesScopeTypesItem]]):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 20.
        sorts (Union[Unset, None, List[ListRolesSortsItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RolesPaginated]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
            include_default_roles=include_default_roles,
            scope_types=scope_types,
            offset=offset,
            limit=limit,
            sorts=sorts,
        )
    ).parsed
