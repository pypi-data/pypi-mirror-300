from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.search_index_response import SearchIndexResponse
from ...models.search_request import SearchRequest
from ...types import Response


def _get_kwargs(
    *,
    body: SearchRequest,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/search/",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, SearchIndexResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SearchIndexResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, SearchIndexResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: SearchRequest,
) -> Response[Union[HTTPValidationError, SearchIndexResponse]]:
    """Search

     综合搜索, 支持搜索站点, 文档, 知识库。返回搜索结果的摘要条目。
    前端，通常点击条目后，打开详细操作页
    参考： https://www.w3cschool.cn/article/34124192.html

    TODO: 可以考虑添加高亮显示的功能。

    Args:
        body (SearchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SearchIndexResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: SearchRequest,
) -> Optional[Union[HTTPValidationError, SearchIndexResponse]]:
    """Search

     综合搜索, 支持搜索站点, 文档, 知识库。返回搜索结果的摘要条目。
    前端，通常点击条目后，打开详细操作页
    参考： https://www.w3cschool.cn/article/34124192.html

    TODO: 可以考虑添加高亮显示的功能。

    Args:
        body (SearchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SearchIndexResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: SearchRequest,
) -> Response[Union[HTTPValidationError, SearchIndexResponse]]:
    """Search

     综合搜索, 支持搜索站点, 文档, 知识库。返回搜索结果的摘要条目。
    前端，通常点击条目后，打开详细操作页
    参考： https://www.w3cschool.cn/article/34124192.html

    TODO: 可以考虑添加高亮显示的功能。

    Args:
        body (SearchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SearchIndexResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: SearchRequest,
) -> Optional[Union[HTTPValidationError, SearchIndexResponse]]:
    """Search

     综合搜索, 支持搜索站点, 文档, 知识库。返回搜索结果的摘要条目。
    前端，通常点击条目后，打开详细操作页
    参考： https://www.w3cschool.cn/article/34124192.html

    TODO: 可以考虑添加高亮显示的功能。

    Args:
        body (SearchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SearchIndexResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
