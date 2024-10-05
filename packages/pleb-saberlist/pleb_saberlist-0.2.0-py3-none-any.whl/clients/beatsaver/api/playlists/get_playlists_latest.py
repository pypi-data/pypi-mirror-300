import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_playlists_latest_sort import GetPlaylistsLatestSort
from ...models.playlist_search_response import PlaylistSearchResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    after: Union[Unset, datetime.datetime] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    page_size: Union[Unset, int] = 20,
    sort: Union[Unset, GetPlaylistsLatestSort] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_after: Union[Unset, str] = UNSET
    if not isinstance(after, Unset):
        json_after = after.isoformat()
    params["after"] = json_after

    json_before: Union[Unset, str] = UNSET
    if not isinstance(before, Unset):
        json_before = before.isoformat()
    params["before"] = json_before

    params["pageSize"] = page_size

    json_sort: Union[Unset, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/playlists/latest",
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
    *,
    client: Union[AuthenticatedClient, Client],
    after: Union[Unset, datetime.datetime] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    page_size: Union[Unset, int] = 20,
    sort: Union[Unset, GetPlaylistsLatestSort] = UNSET,
) -> Response[PlaylistSearchResponse]:
    """Get playlists ordered by created/updated

    Args:
        after (Union[Unset, datetime.datetime]):
        before (Union[Unset, datetime.datetime]):
        page_size (Union[Unset, int]):  Default: 20.
        sort (Union[Unset, GetPlaylistsLatestSort]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PlaylistSearchResponse]
    """

    kwargs = _get_kwargs(
        after=after,
        before=before,
        page_size=page_size,
        sort=sort,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    after: Union[Unset, datetime.datetime] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    page_size: Union[Unset, int] = 20,
    sort: Union[Unset, GetPlaylistsLatestSort] = UNSET,
) -> Optional[PlaylistSearchResponse]:
    """Get playlists ordered by created/updated

    Args:
        after (Union[Unset, datetime.datetime]):
        before (Union[Unset, datetime.datetime]):
        page_size (Union[Unset, int]):  Default: 20.
        sort (Union[Unset, GetPlaylistsLatestSort]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PlaylistSearchResponse
    """

    return sync_detailed(
        client=client,
        after=after,
        before=before,
        page_size=page_size,
        sort=sort,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    after: Union[Unset, datetime.datetime] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    page_size: Union[Unset, int] = 20,
    sort: Union[Unset, GetPlaylistsLatestSort] = UNSET,
) -> Response[PlaylistSearchResponse]:
    """Get playlists ordered by created/updated

    Args:
        after (Union[Unset, datetime.datetime]):
        before (Union[Unset, datetime.datetime]):
        page_size (Union[Unset, int]):  Default: 20.
        sort (Union[Unset, GetPlaylistsLatestSort]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PlaylistSearchResponse]
    """

    kwargs = _get_kwargs(
        after=after,
        before=before,
        page_size=page_size,
        sort=sort,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    after: Union[Unset, datetime.datetime] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    page_size: Union[Unset, int] = 20,
    sort: Union[Unset, GetPlaylistsLatestSort] = UNSET,
) -> Optional[PlaylistSearchResponse]:
    """Get playlists ordered by created/updated

    Args:
        after (Union[Unset, datetime.datetime]):
        before (Union[Unset, datetime.datetime]):
        page_size (Union[Unset, int]):  Default: 20.
        sort (Union[Unset, GetPlaylistsLatestSort]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PlaylistSearchResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            after=after,
            before=before,
            page_size=page_size,
            sort=sort,
        )
    ).parsed
