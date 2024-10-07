from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_role_templates_scope_types_item import ListRoleTemplatesScopeTypesItem
from ...models.role_template import RoleTemplate
from ...types import UNSET, Response, Unset


def _get_kwargs(
    organization_id: str,
    *,
    scope_types: Union[Unset, None, List[ListRoleTemplatesScopeTypesItem]] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
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

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/organizations/{organizationId}/role-templates".format(
            organizationId=organization_id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, List["RoleTemplate"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = RoleTemplate.from_dict(response_200_item_data)

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
) -> Response[Union[Error, List["RoleTemplate"]]]:
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
    scope_types: Union[Unset, None, List[ListRoleTemplatesScopeTypesItem]] = UNSET,
) -> Response[Union[Error, List["RoleTemplate"]]]:
    """Get role templates

     Get a list of available role templates in an Organization. A role template can be used as the basis
    for creating a new custom role.

    Args:
        organization_id (str):
        scope_types (Union[Unset, None, List[ListRoleTemplatesScopeTypesItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, List['RoleTemplate']]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        scope_types=scope_types,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_id: str,
    *,
    client: AuthenticatedClient,
    scope_types: Union[Unset, None, List[ListRoleTemplatesScopeTypesItem]] = UNSET,
) -> Optional[Union[Error, List["RoleTemplate"]]]:
    """Get role templates

     Get a list of available role templates in an Organization. A role template can be used as the basis
    for creating a new custom role.

    Args:
        organization_id (str):
        scope_types (Union[Unset, None, List[ListRoleTemplatesScopeTypesItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, List['RoleTemplate']]
    """

    return sync_detailed(
        organization_id=organization_id,
        client=client,
        scope_types=scope_types,
    ).parsed


async def asyncio_detailed(
    organization_id: str,
    *,
    client: AuthenticatedClient,
    scope_types: Union[Unset, None, List[ListRoleTemplatesScopeTypesItem]] = UNSET,
) -> Response[Union[Error, List["RoleTemplate"]]]:
    """Get role templates

     Get a list of available role templates in an Organization. A role template can be used as the basis
    for creating a new custom role.

    Args:
        organization_id (str):
        scope_types (Union[Unset, None, List[ListRoleTemplatesScopeTypesItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, List['RoleTemplate']]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        scope_types=scope_types,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_id: str,
    *,
    client: AuthenticatedClient,
    scope_types: Union[Unset, None, List[ListRoleTemplatesScopeTypesItem]] = UNSET,
) -> Optional[Union[Error, List["RoleTemplate"]]]:
    """Get role templates

     Get a list of available role templates in an Organization. A role template can be used as the basis
    for creating a new custom role.

    Args:
        organization_id (str):
        scope_types (Union[Unset, None, List[ListRoleTemplatesScopeTypesItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, List['RoleTemplate']]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
            scope_types=scope_types,
        )
    ).parsed
