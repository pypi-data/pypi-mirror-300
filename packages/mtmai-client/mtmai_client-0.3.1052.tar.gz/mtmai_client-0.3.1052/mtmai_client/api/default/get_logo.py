from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.theme import Theme
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    theme: Union[None, Theme, Unset] = Theme.LIGHT,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_theme: Union[None, Unset, str]
    if isinstance(theme, Unset):
        json_theme = UNSET
    elif isinstance(theme, Theme):
        json_theme = theme.value
    else:
        json_theme = theme
    params["theme"] = json_theme

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/logo",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = response.json()
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
) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    theme: Union[None, Theme, Unset] = Theme.LIGHT,
) -> Response[Union[Any, HTTPValidationError]]:
    """Get Logo

     Get the default logo for the UI.

    Args:
        theme (Union[None, Theme, Unset]):  Default: Theme.LIGHT.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        theme=theme,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    theme: Union[None, Theme, Unset] = Theme.LIGHT,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Get Logo

     Get the default logo for the UI.

    Args:
        theme (Union[None, Theme, Unset]):  Default: Theme.LIGHT.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        theme=theme,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    theme: Union[None, Theme, Unset] = Theme.LIGHT,
) -> Response[Union[Any, HTTPValidationError]]:
    """Get Logo

     Get the default logo for the UI.

    Args:
        theme (Union[None, Theme, Unset]):  Default: Theme.LIGHT.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        theme=theme,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    theme: Union[None, Theme, Unset] = Theme.LIGHT,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Get Logo

     Get the default logo for the UI.

    Args:
        theme (Union[None, Theme, Unset]):  Default: Theme.LIGHT.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            theme=theme,
        )
    ).parsed
