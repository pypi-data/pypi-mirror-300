import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.search_response import SearchResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: int,
    *,
    before: Union[Unset, datetime.datetime] = UNSET,
    page_size: Union[Unset, int] = 20,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_before: Union[Unset, str] = UNSET
    if not isinstance(before, Unset):
        json_before = before.isoformat()
    params["before"] = json_before

    params["pageSize"] = page_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/maps/collaborations/{id}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SearchResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SearchResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SearchResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    before: Union[Unset, datetime.datetime] = UNSET,
    page_size: Union[Unset, int] = 20,
) -> Response[SearchResponse]:
    """Get maps by a user, including collaborations

    Args:
        id (int):
        before (Union[Unset, datetime.datetime]):
        page_size (Union[Unset, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        before=before,
        page_size=page_size,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    before: Union[Unset, datetime.datetime] = UNSET,
    page_size: Union[Unset, int] = 20,
) -> Optional[SearchResponse]:
    """Get maps by a user, including collaborations

    Args:
        id (int):
        before (Union[Unset, datetime.datetime]):
        page_size (Union[Unset, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SearchResponse
    """

    return sync_detailed(
        id=id,
        client=client,
        before=before,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    before: Union[Unset, datetime.datetime] = UNSET,
    page_size: Union[Unset, int] = 20,
) -> Response[SearchResponse]:
    """Get maps by a user, including collaborations

    Args:
        id (int):
        before (Union[Unset, datetime.datetime]):
        page_size (Union[Unset, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        before=before,
        page_size=page_size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    before: Union[Unset, datetime.datetime] = UNSET,
    page_size: Union[Unset, int] = 20,
) -> Optional[SearchResponse]:
    """Get maps by a user, including collaborations

    Args:
        id (int):
        before (Union[Unset, datetime.datetime]):
        page_size (Union[Unset, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SearchResponse
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            before=before,
            page_size=page_size,
        )
    ).parsed
