from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_tokens_paginated import ApiTokensPaginated
from ...models.error import Error
from ...models.list_api_tokens_sorts_item import ListApiTokensSortsItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    organization_id: str,
    *,
    workspace_id: Union[Unset, None, str] = UNSET,
    deployment_id: Union[Unset, None, str] = UNSET,
    include_only_organization_tokens: Union[Unset, None, bool] = UNSET,
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 20,
    sorts: Union[Unset, None, List[ListApiTokensSortsItem]] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["workspaceId"] = workspace_id

    params["deploymentId"] = deployment_id

    params["includeOnlyOrganizationTokens"] = include_only_organization_tokens

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
        "url": "/organizations/{organizationId}/tokens".format(
            organizationId=organization_id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ApiTokensPaginated, Error]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ApiTokensPaginated.from_dict(response.json())

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
) -> Response[Union[ApiTokensPaginated, Error]]:
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
    workspace_id: Union[Unset, None, str] = UNSET,
    deployment_id: Union[Unset, None, str] = UNSET,
    include_only_organization_tokens: Union[Unset, None, bool] = UNSET,
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 20,
    sorts: Union[Unset, None, List[ListApiTokensSortsItem]] = UNSET,
) -> Response[Union[ApiTokensPaginated, Error]]:
    """List API tokens

     List information about all API tokens from an Organization. Filters on Workspace when Workspace ID
    is provided. When `includeOnlyOrganizationTokens` is `true`, only Organization API tokens are
    returned.

    Args:
        organization_id (str):
        workspace_id (Union[Unset, None, str]):
        deployment_id (Union[Unset, None, str]):
        include_only_organization_tokens (Union[Unset, None, bool]):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 20.
        sorts (Union[Unset, None, List[ListApiTokensSortsItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiTokensPaginated, Error]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        workspace_id=workspace_id,
        deployment_id=deployment_id,
        include_only_organization_tokens=include_only_organization_tokens,
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
    workspace_id: Union[Unset, None, str] = UNSET,
    deployment_id: Union[Unset, None, str] = UNSET,
    include_only_organization_tokens: Union[Unset, None, bool] = UNSET,
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 20,
    sorts: Union[Unset, None, List[ListApiTokensSortsItem]] = UNSET,
) -> Optional[Union[ApiTokensPaginated, Error]]:
    """List API tokens

     List information about all API tokens from an Organization. Filters on Workspace when Workspace ID
    is provided. When `includeOnlyOrganizationTokens` is `true`, only Organization API tokens are
    returned.

    Args:
        organization_id (str):
        workspace_id (Union[Unset, None, str]):
        deployment_id (Union[Unset, None, str]):
        include_only_organization_tokens (Union[Unset, None, bool]):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 20.
        sorts (Union[Unset, None, List[ListApiTokensSortsItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiTokensPaginated, Error]
    """

    return sync_detailed(
        organization_id=organization_id,
        client=client,
        workspace_id=workspace_id,
        deployment_id=deployment_id,
        include_only_organization_tokens=include_only_organization_tokens,
        offset=offset,
        limit=limit,
        sorts=sorts,
    ).parsed


async def asyncio_detailed(
    organization_id: str,
    *,
    client: AuthenticatedClient,
    workspace_id: Union[Unset, None, str] = UNSET,
    deployment_id: Union[Unset, None, str] = UNSET,
    include_only_organization_tokens: Union[Unset, None, bool] = UNSET,
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 20,
    sorts: Union[Unset, None, List[ListApiTokensSortsItem]] = UNSET,
) -> Response[Union[ApiTokensPaginated, Error]]:
    """List API tokens

     List information about all API tokens from an Organization. Filters on Workspace when Workspace ID
    is provided. When `includeOnlyOrganizationTokens` is `true`, only Organization API tokens are
    returned.

    Args:
        organization_id (str):
        workspace_id (Union[Unset, None, str]):
        deployment_id (Union[Unset, None, str]):
        include_only_organization_tokens (Union[Unset, None, bool]):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 20.
        sorts (Union[Unset, None, List[ListApiTokensSortsItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiTokensPaginated, Error]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        workspace_id=workspace_id,
        deployment_id=deployment_id,
        include_only_organization_tokens=include_only_organization_tokens,
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
    workspace_id: Union[Unset, None, str] = UNSET,
    deployment_id: Union[Unset, None, str] = UNSET,
    include_only_organization_tokens: Union[Unset, None, bool] = UNSET,
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 20,
    sorts: Union[Unset, None, List[ListApiTokensSortsItem]] = UNSET,
) -> Optional[Union[ApiTokensPaginated, Error]]:
    """List API tokens

     List information about all API tokens from an Organization. Filters on Workspace when Workspace ID
    is provided. When `includeOnlyOrganizationTokens` is `true`, only Organization API tokens are
    returned.

    Args:
        organization_id (str):
        workspace_id (Union[Unset, None, str]):
        deployment_id (Union[Unset, None, str]):
        include_only_organization_tokens (Union[Unset, None, bool]):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 20.
        sorts (Union[Unset, None, List[ListApiTokensSortsItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiTokensPaginated, Error]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
            workspace_id=workspace_id,
            deployment_id=deployment_id,
            include_only_organization_tokens=include_only_organization_tokens,
            offset=offset,
            limit=limit,
            sorts=sorts,
        )
    ).parsed
