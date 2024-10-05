import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_playlists_search_page_sort_order import GetPlaylistsSearchPageSortOrder
from ...models.playlist_search_response import PlaylistSearchResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    page: int = 0,
    *,
    curated: Union[Unset, bool] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    include_empty: Union[Unset, bool] = UNSET,
    max_nps: Union[Unset, Any] = UNSET,
    min_nps: Union[Unset, Any] = UNSET,
    q: Union[Unset, str] = UNSET,
    sort_order: GetPlaylistsSearchPageSortOrder,
    to: Union[Unset, datetime.datetime] = UNSET,
    verified: Union[Unset, bool] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["curated"] = curated

    json_from_: Union[Unset, str] = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat()
    params["from"] = json_from_

    params["includeEmpty"] = include_empty

    params["maxNps"] = max_nps

    params["minNps"] = min_nps

    params["q"] = q

    json_sort_order = sort_order.value
    params["sortOrder"] = json_sort_order

    json_to: Union[Unset, str] = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat()
    params["to"] = json_to

    params["verified"] = verified

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/playlists/search/{page}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[PlaylistSearchResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PlaylistSearchResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[PlaylistSearchResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    page: int = 0,
    *,
    client: Union[AuthenticatedClient, Client],
    curated: Union[Unset, bool] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    include_empty: Union[Unset, bool] = UNSET,
    max_nps: Union[Unset, Any] = UNSET,
    min_nps: Union[Unset, Any] = UNSET,
    q: Union[Unset, str] = UNSET,
    sort_order: GetPlaylistsSearchPageSortOrder,
    to: Union[Unset, datetime.datetime] = UNSET,
    verified: Union[Unset, bool] = UNSET,
) -> Response[PlaylistSearchResponse]:
    """Search for playlists

    Args:
        page (int):  Default: 0.
        curated (Union[Unset, bool]):
        from_ (Union[Unset, datetime.datetime]):
        include_empty (Union[Unset, bool]):
        max_nps (Union[Unset, Any]):
        min_nps (Union[Unset, Any]):
        q (Union[Unset, str]):
        sort_order (GetPlaylistsSearchPageSortOrder):
        to (Union[Unset, datetime.datetime]):
        verified (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PlaylistSearchResponse]
    """

    kwargs = _get_kwargs(
        page=page,
        curated=curated,
        from_=from_,
        include_empty=include_empty,
        max_nps=max_nps,
        min_nps=min_nps,
        q=q,
        sort_order=sort_order,
        to=to,
        verified=verified,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    page: int = 0,
    *,
    client: Union[AuthenticatedClient, Client],
    curated: Union[Unset, bool] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    include_empty: Union[Unset, bool] = UNSET,
    max_nps: Union[Unset, Any] = UNSET,
    min_nps: Union[Unset, Any] = UNSET,
    q: Union[Unset, str] = UNSET,
    sort_order: GetPlaylistsSearchPageSortOrder,
    to: Union[Unset, datetime.datetime] = UNSET,
    verified: Union[Unset, bool] = UNSET,
) -> Optional[PlaylistSearchResponse]:
    """Search for playlists

    Args:
        page (int):  Default: 0.
        curated (Union[Unset, bool]):
        from_ (Union[Unset, datetime.datetime]):
        include_empty (Union[Unset, bool]):
        max_nps (Union[Unset, Any]):
        min_nps (Union[Unset, Any]):
        q (Union[Unset, str]):
        sort_order (GetPlaylistsSearchPageSortOrder):
        to (Union[Unset, datetime.datetime]):
        verified (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PlaylistSearchResponse
    """

    return sync_detailed(
        page=page,
        client=client,
        curated=curated,
        from_=from_,
        include_empty=include_empty,
        max_nps=max_nps,
        min_nps=min_nps,
        q=q,
        sort_order=sort_order,
        to=to,
        verified=verified,
    ).parsed


async def asyncio_detailed(
    page: int = 0,
    *,
    client: Union[AuthenticatedClient, Client],
    curated: Union[Unset, bool] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    include_empty: Union[Unset, bool] = UNSET,
    max_nps: Union[Unset, Any] = UNSET,
    min_nps: Union[Unset, Any] = UNSET,
    q: Union[Unset, str] = UNSET,
    sort_order: GetPlaylistsSearchPageSortOrder,
    to: Union[Unset, datetime.datetime] = UNSET,
    verified: Union[Unset, bool] = UNSET,
) -> Response[PlaylistSearchResponse]:
    """Search for playlists

    Args:
        page (int):  Default: 0.
        curated (Union[Unset, bool]):
        from_ (Union[Unset, datetime.datetime]):
        include_empty (Union[Unset, bool]):
        max_nps (Union[Unset, Any]):
        min_nps (Union[Unset, Any]):
        q (Union[Unset, str]):
        sort_order (GetPlaylistsSearchPageSortOrder):
        to (Union[Unset, datetime.datetime]):
        verified (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PlaylistSearchResponse]
    """

    kwargs = _get_kwargs(
        page=page,
        curated=curated,
        from_=from_,
        include_empty=include_empty,
        max_nps=max_nps,
        min_nps=min_nps,
        q=q,
        sort_order=sort_order,
        to=to,
        verified=verified,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    page: int = 0,
    *,
    client: Union[AuthenticatedClient, Client],
    curated: Union[Unset, bool] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    include_empty: Union[Unset, bool] = UNSET,
    max_nps: Union[Unset, Any] = UNSET,
    min_nps: Union[Unset, Any] = UNSET,
    q: Union[Unset, str] = UNSET,
    sort_order: GetPlaylistsSearchPageSortOrder,
    to: Union[Unset, datetime.datetime] = UNSET,
    verified: Union[Unset, bool] = UNSET,
) -> Optional[PlaylistSearchResponse]:
    """Search for playlists

    Args:
        page (int):  Default: 0.
        curated (Union[Unset, bool]):
        from_ (Union[Unset, datetime.datetime]):
        include_empty (Union[Unset, bool]):
        max_nps (Union[Unset, Any]):
        min_nps (Union[Unset, Any]):
        q (Union[Unset, str]):
        sort_order (GetPlaylistsSearchPageSortOrder):
        to (Union[Unset, datetime.datetime]):
        verified (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PlaylistSearchResponse
    """

    return (
        await asyncio_detailed(
            page=page,
            client=client,
            curated=curated,
            from_=from_,
            include_empty=include_empty,
            max_nps=max_nps,
            min_nps=min_nps,
            q=q,
            sort_order=sort_order,
            to=to,
            verified=verified,
        )
    ).parsed
