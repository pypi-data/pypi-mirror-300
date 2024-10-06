from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.tag_list_response import TagListResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    site_id: Union[None, Unset, str] = UNSET,
    query: Union[Unset, str] = "",
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_site_id: Union[None, Unset, str]
    if isinstance(site_id, Unset):
        json_site_id = UNSET
    else:
        json_site_id = site_id
    params["siteId"] = json_site_id

    params["query"] = query

    params["offset"] = offset

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/site/tags/list",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, TagListResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TagListResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, TagListResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    site_id: Union[None, Unset, str] = UNSET,
    query: Union[Unset, str] = "",
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[HTTPValidationError, TagListResponse]]:
    """Tab List

    Args:
        site_id (Union[None, Unset, str]):
        query (Union[Unset, str]):  Default: ''.
        offset (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TagListResponse]]
    """

    kwargs = _get_kwargs(
        site_id=site_id,
        query=query,
        offset=offset,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    site_id: Union[None, Unset, str] = UNSET,
    query: Union[Unset, str] = "",
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, TagListResponse]]:
    """Tab List

    Args:
        site_id (Union[None, Unset, str]):
        query (Union[Unset, str]):  Default: ''.
        offset (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TagListResponse]
    """

    return sync_detailed(
        client=client,
        site_id=site_id,
        query=query,
        offset=offset,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    site_id: Union[None, Unset, str] = UNSET,
    query: Union[Unset, str] = "",
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[HTTPValidationError, TagListResponse]]:
    """Tab List

    Args:
        site_id (Union[None, Unset, str]):
        query (Union[Unset, str]):  Default: ''.
        offset (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TagListResponse]]
    """

    kwargs = _get_kwargs(
        site_id=site_id,
        query=query,
        offset=offset,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    site_id: Union[None, Unset, str] = UNSET,
    query: Union[Unset, str] = "",
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, TagListResponse]]:
    """Tab List

    Args:
        site_id (Union[None, Unset, str]):
        query (Union[Unset, str]):  Default: ''.
        offset (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TagListResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            site_id=site_id,
            query=query,
            offset=offset,
            limit=limit,
        )
    ).parsed
