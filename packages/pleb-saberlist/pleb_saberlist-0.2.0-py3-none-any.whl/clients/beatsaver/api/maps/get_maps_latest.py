import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_maps_latest_sort import GetMapsLatestSort
from ...models.search_response import SearchResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    after: Union[Unset, datetime.datetime] = UNSET,
    automapper: Union[Unset, bool] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    page_size: Union[Unset, int] = 20,
    sort: Union[Unset, GetMapsLatestSort] = UNSET,
    verified: Union[Unset, bool] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_after: Union[Unset, str] = UNSET
    if not isinstance(after, Unset):
        json_after = after.isoformat()
    params["after"] = json_after

    params["automapper"] = automapper

    json_before: Union[Unset, str] = UNSET
    if not isinstance(before, Unset):
        json_before = before.isoformat()
    params["before"] = json_before

    params["pageSize"] = page_size

    json_sort: Union[Unset, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params["verified"] = verified

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/maps/latest",
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
    *,
    client: Union[AuthenticatedClient, Client],
    after: Union[Unset, datetime.datetime] = UNSET,
    automapper: Union[Unset, bool] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    page_size: Union[Unset, int] = 20,
    sort: Union[Unset, GetMapsLatestSort] = UNSET,
    verified: Union[Unset, bool] = UNSET,
) -> Response[SearchResponse]:
    """Get maps ordered by upload/publish/updated. If you're going to scrape the data and make 100s of
    requests make this this endpoint you use.

    Args:
        after (Union[Unset, datetime.datetime]):
        automapper (Union[Unset, bool]):
        before (Union[Unset, datetime.datetime]):
        page_size (Union[Unset, int]):  Default: 20.
        sort (Union[Unset, GetMapsLatestSort]):
        verified (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchResponse]
    """

    kwargs = _get_kwargs(
        after=after,
        automapper=automapper,
        before=before,
        page_size=page_size,
        sort=sort,
        verified=verified,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    after: Union[Unset, datetime.datetime] = UNSET,
    automapper: Union[Unset, bool] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    page_size: Union[Unset, int] = 20,
    sort: Union[Unset, GetMapsLatestSort] = UNSET,
    verified: Union[Unset, bool] = UNSET,
) -> Optional[SearchResponse]:
    """Get maps ordered by upload/publish/updated. If you're going to scrape the data and make 100s of
    requests make this this endpoint you use.

    Args:
        after (Union[Unset, datetime.datetime]):
        automapper (Union[Unset, bool]):
        before (Union[Unset, datetime.datetime]):
        page_size (Union[Unset, int]):  Default: 20.
        sort (Union[Unset, GetMapsLatestSort]):
        verified (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SearchResponse
    """

    return sync_detailed(
        client=client,
        after=after,
        automapper=automapper,
        before=before,
        page_size=page_size,
        sort=sort,
        verified=verified,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    after: Union[Unset, datetime.datetime] = UNSET,
    automapper: Union[Unset, bool] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    page_size: Union[Unset, int] = 20,
    sort: Union[Unset, GetMapsLatestSort] = UNSET,
    verified: Union[Unset, bool] = UNSET,
) -> Response[SearchResponse]:
    """Get maps ordered by upload/publish/updated. If you're going to scrape the data and make 100s of
    requests make this this endpoint you use.

    Args:
        after (Union[Unset, datetime.datetime]):
        automapper (Union[Unset, bool]):
        before (Union[Unset, datetime.datetime]):
        page_size (Union[Unset, int]):  Default: 20.
        sort (Union[Unset, GetMapsLatestSort]):
        verified (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchResponse]
    """

    kwargs = _get_kwargs(
        after=after,
        automapper=automapper,
        before=before,
        page_size=page_size,
        sort=sort,
        verified=verified,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    after: Union[Unset, datetime.datetime] = UNSET,
    automapper: Union[Unset, bool] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    page_size: Union[Unset, int] = 20,
    sort: Union[Unset, GetMapsLatestSort] = UNSET,
    verified: Union[Unset, bool] = UNSET,
) -> Optional[SearchResponse]:
    """Get maps ordered by upload/publish/updated. If you're going to scrape the data and make 100s of
    requests make this this endpoint you use.

    Args:
        after (Union[Unset, datetime.datetime]):
        automapper (Union[Unset, bool]):
        before (Union[Unset, datetime.datetime]):
        page_size (Union[Unset, int]):  Default: 20.
        sort (Union[Unset, GetMapsLatestSort]):
        verified (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SearchResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            after=after,
            automapper=automapper,
            before=before,
            page_size=page_size,
            sort=sort,
            verified=verified,
        )
    ).parsed
