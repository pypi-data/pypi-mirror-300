from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.allowed_ip_address_ranges_paginated import AllowedIpAddressRangesPaginated
from ...models.error import Error
from ...models.list_allowed_ip_address_ranges_sorts_item import ListAllowedIpAddressRangesSortsItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    organization_id: str,
    *,
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 20,
    sorts: Union[Unset, None, List[ListAllowedIpAddressRangesSortsItem]] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
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
        "url": "/organizations/{organizationId}/allowed-ip-address-ranges".format(
            organizationId=organization_id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AllowedIpAddressRangesPaginated, Error]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AllowedIpAddressRangesPaginated.from_dict(response.json())

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
) -> Response[Union[AllowedIpAddressRangesPaginated, Error]]:
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
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 20,
    sorts: Union[Unset, None, List[ListAllowedIpAddressRangesSortsItem]] = UNSET,
) -> Response[Union[AllowedIpAddressRangesPaginated, Error]]:
    """List allowed IP address ranges

     List allowed IP address ranges.

    Args:
        organization_id (str):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 20.
        sorts (Union[Unset, None, List[ListAllowedIpAddressRangesSortsItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AllowedIpAddressRangesPaginated, Error]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
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
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 20,
    sorts: Union[Unset, None, List[ListAllowedIpAddressRangesSortsItem]] = UNSET,
) -> Optional[Union[AllowedIpAddressRangesPaginated, Error]]:
    """List allowed IP address ranges

     List allowed IP address ranges.

    Args:
        organization_id (str):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 20.
        sorts (Union[Unset, None, List[ListAllowedIpAddressRangesSortsItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AllowedIpAddressRangesPaginated, Error]
    """

    return sync_detailed(
        organization_id=organization_id,
        client=client,
        offset=offset,
        limit=limit,
        sorts=sorts,
    ).parsed


async def asyncio_detailed(
    organization_id: str,
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 20,
    sorts: Union[Unset, None, List[ListAllowedIpAddressRangesSortsItem]] = UNSET,
) -> Response[Union[AllowedIpAddressRangesPaginated, Error]]:
    """List allowed IP address ranges

     List allowed IP address ranges.

    Args:
        organization_id (str):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 20.
        sorts (Union[Unset, None, List[ListAllowedIpAddressRangesSortsItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AllowedIpAddressRangesPaginated, Error]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
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
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 20,
    sorts: Union[Unset, None, List[ListAllowedIpAddressRangesSortsItem]] = UNSET,
) -> Optional[Union[AllowedIpAddressRangesPaginated, Error]]:
    """List allowed IP address ranges

     List allowed IP address ranges.

    Args:
        organization_id (str):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 20.
        sorts (Union[Unset, None, List[ListAllowedIpAddressRangesSortsItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AllowedIpAddressRangesPaginated, Error]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
            offset=offset,
            limit=limit,
            sorts=sorts,
        )
    ).parsed
