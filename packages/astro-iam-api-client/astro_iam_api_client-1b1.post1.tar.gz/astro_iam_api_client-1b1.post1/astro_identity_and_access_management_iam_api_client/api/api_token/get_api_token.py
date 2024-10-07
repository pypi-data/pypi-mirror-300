from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_token import ApiToken
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    organization_id: str,
    token_id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/organizations/{organizationId}/tokens/{tokenId}".format(
            organizationId=organization_id,
            tokenId=token_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ApiToken, Error]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ApiToken.from_dict(response.json())

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
) -> Response[Union[ApiToken, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    organization_id: str,
    token_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[ApiToken, Error]]:
    """Get an API token

     Retrieve information about a specific API token.

    Args:
        organization_id (str):
        token_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiToken, Error]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        token_id=token_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_id: str,
    token_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ApiToken, Error]]:
    """Get an API token

     Retrieve information about a specific API token.

    Args:
        organization_id (str):
        token_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiToken, Error]
    """

    return sync_detailed(
        organization_id=organization_id,
        token_id=token_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    organization_id: str,
    token_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[ApiToken, Error]]:
    """Get an API token

     Retrieve information about a specific API token.

    Args:
        organization_id (str):
        token_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiToken, Error]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        token_id=token_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_id: str,
    token_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ApiToken, Error]]:
    """Get an API token

     Retrieve information about a specific API token.

    Args:
        organization_id (str):
        token_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiToken, Error]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            token_id=token_id,
            client=client,
        )
    ).parsed
