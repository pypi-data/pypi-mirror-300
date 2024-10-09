from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.list_site_hosts_response import ListSiteHostsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    q: Union[None, Unset, str] = UNSET,
    site_id: Union[None, Unset, str] = UNSET,
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_q: Union[None, Unset, str]
    if isinstance(q, Unset):
        json_q = UNSET
    else:
        json_q = q
    params["q"] = json_q

    json_site_id: Union[None, Unset, str]
    if isinstance(site_id, Unset):
        json_site_id = UNSET
    else:
        json_site_id = site_id
    params["siteId"] = json_site_id

    params["skip"] = skip

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/site/hosts",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ListSiteHostsResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListSiteHostsResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, ListSiteHostsResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    q: Union[None, Unset, str] = UNSET,
    site_id: Union[None, Unset, str] = UNSET,
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[HTTPValidationError, ListSiteHostsResponse]]:
    """List Site Hosts

     Retrieve site hosts.

    Args:
        q (Union[None, Unset, str]):
        site_id (Union[None, Unset, str]):
        skip (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ListSiteHostsResponse]]
    """

    kwargs = _get_kwargs(
        q=q,
        site_id=site_id,
        skip=skip,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    q: Union[None, Unset, str] = UNSET,
    site_id: Union[None, Unset, str] = UNSET,
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, ListSiteHostsResponse]]:
    """List Site Hosts

     Retrieve site hosts.

    Args:
        q (Union[None, Unset, str]):
        site_id (Union[None, Unset, str]):
        skip (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ListSiteHostsResponse]
    """

    return sync_detailed(
        client=client,
        q=q,
        site_id=site_id,
        skip=skip,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    q: Union[None, Unset, str] = UNSET,
    site_id: Union[None, Unset, str] = UNSET,
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[HTTPValidationError, ListSiteHostsResponse]]:
    """List Site Hosts

     Retrieve site hosts.

    Args:
        q (Union[None, Unset, str]):
        site_id (Union[None, Unset, str]):
        skip (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ListSiteHostsResponse]]
    """

    kwargs = _get_kwargs(
        q=q,
        site_id=site_id,
        skip=skip,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    q: Union[None, Unset, str] = UNSET,
    site_id: Union[None, Unset, str] = UNSET,
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, ListSiteHostsResponse]]:
    """List Site Hosts

     Retrieve site hosts.

    Args:
        q (Union[None, Unset, str]):
        site_id (Union[None, Unset, str]):
        skip (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ListSiteHostsResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            q=q,
            site_id=site_id,
            skip=skip,
            limit=limit,
        )
    ).parsed
