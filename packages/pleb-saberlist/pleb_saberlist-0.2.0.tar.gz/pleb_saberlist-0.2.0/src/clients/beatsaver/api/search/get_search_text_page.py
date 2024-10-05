import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_search_text_page_leaderboard import GetSearchTextPageLeaderboard
from ...models.get_search_text_page_sort_order import GetSearchTextPageSortOrder
from ...models.search_response import SearchResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    page: int = 0,
    *,
    automapper: Union[Unset, bool] = UNSET,
    chroma: Union[Unset, bool] = UNSET,
    cinema: Union[Unset, bool] = UNSET,
    curated: Union[Unset, bool] = UNSET,
    followed: Union[Unset, bool] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    full_spread: Union[Unset, bool] = UNSET,
    leaderboard: GetSearchTextPageLeaderboard,
    max_bpm: Union[Unset, Any] = UNSET,
    max_duration: Union[Unset, int] = UNSET,
    max_nps: Union[Unset, Any] = UNSET,
    max_rating: Union[Unset, Any] = UNSET,
    me: Union[Unset, bool] = UNSET,
    min_bpm: Union[Unset, Any] = UNSET,
    min_duration: Union[Unset, int] = UNSET,
    min_nps: Union[Unset, Any] = UNSET,
    min_rating: Union[Unset, Any] = UNSET,
    noodle: Union[Unset, bool] = UNSET,
    q: Union[Unset, str] = UNSET,
    sort_order: GetSearchTextPageSortOrder,
    tags: Union[Unset, str] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    verified: Union[Unset, bool] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["automapper"] = automapper

    params["chroma"] = chroma

    params["cinema"] = cinema

    params["curated"] = curated

    params["followed"] = followed

    json_from_: Union[Unset, str] = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat()
    params["from"] = json_from_

    params["fullSpread"] = full_spread

    json_leaderboard = leaderboard.value
    params["leaderboard"] = json_leaderboard

    params["maxBpm"] = max_bpm

    params["maxDuration"] = max_duration

    params["maxNps"] = max_nps

    params["maxRating"] = max_rating

    params["me"] = me

    params["minBpm"] = min_bpm

    params["minDuration"] = min_duration

    params["minNps"] = min_nps

    params["minRating"] = min_rating

    params["noodle"] = noodle

    params["q"] = q

    json_sort_order = sort_order.value
    params["sortOrder"] = json_sort_order

    params["tags"] = tags

    json_to: Union[Unset, str] = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat()
    params["to"] = json_to

    params["verified"] = verified

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/search/text/{page}",
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
    page: int = 0,
    *,
    client: Union[AuthenticatedClient, Client],
    automapper: Union[Unset, bool] = UNSET,
    chroma: Union[Unset, bool] = UNSET,
    cinema: Union[Unset, bool] = UNSET,
    curated: Union[Unset, bool] = UNSET,
    followed: Union[Unset, bool] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    full_spread: Union[Unset, bool] = UNSET,
    leaderboard: GetSearchTextPageLeaderboard,
    max_bpm: Union[Unset, Any] = UNSET,
    max_duration: Union[Unset, int] = UNSET,
    max_nps: Union[Unset, Any] = UNSET,
    max_rating: Union[Unset, Any] = UNSET,
    me: Union[Unset, bool] = UNSET,
    min_bpm: Union[Unset, Any] = UNSET,
    min_duration: Union[Unset, int] = UNSET,
    min_nps: Union[Unset, Any] = UNSET,
    min_rating: Union[Unset, Any] = UNSET,
    noodle: Union[Unset, bool] = UNSET,
    q: Union[Unset, str] = UNSET,
    sort_order: GetSearchTextPageSortOrder,
    tags: Union[Unset, str] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    verified: Union[Unset, bool] = UNSET,
) -> Response[SearchResponse]:
    """Search for maps

    Args:
        page (int):  Default: 0.
        automapper (Union[Unset, bool]):
        chroma (Union[Unset, bool]):
        cinema (Union[Unset, bool]):
        curated (Union[Unset, bool]):
        followed (Union[Unset, bool]):
        from_ (Union[Unset, datetime.datetime]):
        full_spread (Union[Unset, bool]):
        leaderboard (GetSearchTextPageLeaderboard):
        max_bpm (Union[Unset, Any]):
        max_duration (Union[Unset, int]):
        max_nps (Union[Unset, Any]):
        max_rating (Union[Unset, Any]):
        me (Union[Unset, bool]):
        min_bpm (Union[Unset, Any]):
        min_duration (Union[Unset, int]):
        min_nps (Union[Unset, Any]):
        min_rating (Union[Unset, Any]):
        noodle (Union[Unset, bool]):
        q (Union[Unset, str]):
        sort_order (GetSearchTextPageSortOrder):
        tags (Union[Unset, str]):
        to (Union[Unset, datetime.datetime]):
        verified (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchResponse]
    """

    kwargs = _get_kwargs(
        page=page,
        automapper=automapper,
        chroma=chroma,
        cinema=cinema,
        curated=curated,
        followed=followed,
        from_=from_,
        full_spread=full_spread,
        leaderboard=leaderboard,
        max_bpm=max_bpm,
        max_duration=max_duration,
        max_nps=max_nps,
        max_rating=max_rating,
        me=me,
        min_bpm=min_bpm,
        min_duration=min_duration,
        min_nps=min_nps,
        min_rating=min_rating,
        noodle=noodle,
        q=q,
        sort_order=sort_order,
        tags=tags,
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
    automapper: Union[Unset, bool] = UNSET,
    chroma: Union[Unset, bool] = UNSET,
    cinema: Union[Unset, bool] = UNSET,
    curated: Union[Unset, bool] = UNSET,
    followed: Union[Unset, bool] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    full_spread: Union[Unset, bool] = UNSET,
    leaderboard: GetSearchTextPageLeaderboard,
    max_bpm: Union[Unset, Any] = UNSET,
    max_duration: Union[Unset, int] = UNSET,
    max_nps: Union[Unset, Any] = UNSET,
    max_rating: Union[Unset, Any] = UNSET,
    me: Union[Unset, bool] = UNSET,
    min_bpm: Union[Unset, Any] = UNSET,
    min_duration: Union[Unset, int] = UNSET,
    min_nps: Union[Unset, Any] = UNSET,
    min_rating: Union[Unset, Any] = UNSET,
    noodle: Union[Unset, bool] = UNSET,
    q: Union[Unset, str] = UNSET,
    sort_order: GetSearchTextPageSortOrder,
    tags: Union[Unset, str] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    verified: Union[Unset, bool] = UNSET,
) -> Optional[SearchResponse]:
    """Search for maps

    Args:
        page (int):  Default: 0.
        automapper (Union[Unset, bool]):
        chroma (Union[Unset, bool]):
        cinema (Union[Unset, bool]):
        curated (Union[Unset, bool]):
        followed (Union[Unset, bool]):
        from_ (Union[Unset, datetime.datetime]):
        full_spread (Union[Unset, bool]):
        leaderboard (GetSearchTextPageLeaderboard):
        max_bpm (Union[Unset, Any]):
        max_duration (Union[Unset, int]):
        max_nps (Union[Unset, Any]):
        max_rating (Union[Unset, Any]):
        me (Union[Unset, bool]):
        min_bpm (Union[Unset, Any]):
        min_duration (Union[Unset, int]):
        min_nps (Union[Unset, Any]):
        min_rating (Union[Unset, Any]):
        noodle (Union[Unset, bool]):
        q (Union[Unset, str]):
        sort_order (GetSearchTextPageSortOrder):
        tags (Union[Unset, str]):
        to (Union[Unset, datetime.datetime]):
        verified (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SearchResponse
    """

    return sync_detailed(
        page=page,
        client=client,
        automapper=automapper,
        chroma=chroma,
        cinema=cinema,
        curated=curated,
        followed=followed,
        from_=from_,
        full_spread=full_spread,
        leaderboard=leaderboard,
        max_bpm=max_bpm,
        max_duration=max_duration,
        max_nps=max_nps,
        max_rating=max_rating,
        me=me,
        min_bpm=min_bpm,
        min_duration=min_duration,
        min_nps=min_nps,
        min_rating=min_rating,
        noodle=noodle,
        q=q,
        sort_order=sort_order,
        tags=tags,
        to=to,
        verified=verified,
    ).parsed


async def asyncio_detailed(
    page: int = 0,
    *,
    client: Union[AuthenticatedClient, Client],
    automapper: Union[Unset, bool] = UNSET,
    chroma: Union[Unset, bool] = UNSET,
    cinema: Union[Unset, bool] = UNSET,
    curated: Union[Unset, bool] = UNSET,
    followed: Union[Unset, bool] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    full_spread: Union[Unset, bool] = UNSET,
    leaderboard: GetSearchTextPageLeaderboard,
    max_bpm: Union[Unset, Any] = UNSET,
    max_duration: Union[Unset, int] = UNSET,
    max_nps: Union[Unset, Any] = UNSET,
    max_rating: Union[Unset, Any] = UNSET,
    me: Union[Unset, bool] = UNSET,
    min_bpm: Union[Unset, Any] = UNSET,
    min_duration: Union[Unset, int] = UNSET,
    min_nps: Union[Unset, Any] = UNSET,
    min_rating: Union[Unset, Any] = UNSET,
    noodle: Union[Unset, bool] = UNSET,
    q: Union[Unset, str] = UNSET,
    sort_order: GetSearchTextPageSortOrder,
    tags: Union[Unset, str] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    verified: Union[Unset, bool] = UNSET,
) -> Response[SearchResponse]:
    """Search for maps

    Args:
        page (int):  Default: 0.
        automapper (Union[Unset, bool]):
        chroma (Union[Unset, bool]):
        cinema (Union[Unset, bool]):
        curated (Union[Unset, bool]):
        followed (Union[Unset, bool]):
        from_ (Union[Unset, datetime.datetime]):
        full_spread (Union[Unset, bool]):
        leaderboard (GetSearchTextPageLeaderboard):
        max_bpm (Union[Unset, Any]):
        max_duration (Union[Unset, int]):
        max_nps (Union[Unset, Any]):
        max_rating (Union[Unset, Any]):
        me (Union[Unset, bool]):
        min_bpm (Union[Unset, Any]):
        min_duration (Union[Unset, int]):
        min_nps (Union[Unset, Any]):
        min_rating (Union[Unset, Any]):
        noodle (Union[Unset, bool]):
        q (Union[Unset, str]):
        sort_order (GetSearchTextPageSortOrder):
        tags (Union[Unset, str]):
        to (Union[Unset, datetime.datetime]):
        verified (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchResponse]
    """

    kwargs = _get_kwargs(
        page=page,
        automapper=automapper,
        chroma=chroma,
        cinema=cinema,
        curated=curated,
        followed=followed,
        from_=from_,
        full_spread=full_spread,
        leaderboard=leaderboard,
        max_bpm=max_bpm,
        max_duration=max_duration,
        max_nps=max_nps,
        max_rating=max_rating,
        me=me,
        min_bpm=min_bpm,
        min_duration=min_duration,
        min_nps=min_nps,
        min_rating=min_rating,
        noodle=noodle,
        q=q,
        sort_order=sort_order,
        tags=tags,
        to=to,
        verified=verified,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    page: int = 0,
    *,
    client: Union[AuthenticatedClient, Client],
    automapper: Union[Unset, bool] = UNSET,
    chroma: Union[Unset, bool] = UNSET,
    cinema: Union[Unset, bool] = UNSET,
    curated: Union[Unset, bool] = UNSET,
    followed: Union[Unset, bool] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    full_spread: Union[Unset, bool] = UNSET,
    leaderboard: GetSearchTextPageLeaderboard,
    max_bpm: Union[Unset, Any] = UNSET,
    max_duration: Union[Unset, int] = UNSET,
    max_nps: Union[Unset, Any] = UNSET,
    max_rating: Union[Unset, Any] = UNSET,
    me: Union[Unset, bool] = UNSET,
    min_bpm: Union[Unset, Any] = UNSET,
    min_duration: Union[Unset, int] = UNSET,
    min_nps: Union[Unset, Any] = UNSET,
    min_rating: Union[Unset, Any] = UNSET,
    noodle: Union[Unset, bool] = UNSET,
    q: Union[Unset, str] = UNSET,
    sort_order: GetSearchTextPageSortOrder,
    tags: Union[Unset, str] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    verified: Union[Unset, bool] = UNSET,
) -> Optional[SearchResponse]:
    """Search for maps

    Args:
        page (int):  Default: 0.
        automapper (Union[Unset, bool]):
        chroma (Union[Unset, bool]):
        cinema (Union[Unset, bool]):
        curated (Union[Unset, bool]):
        followed (Union[Unset, bool]):
        from_ (Union[Unset, datetime.datetime]):
        full_spread (Union[Unset, bool]):
        leaderboard (GetSearchTextPageLeaderboard):
        max_bpm (Union[Unset, Any]):
        max_duration (Union[Unset, int]):
        max_nps (Union[Unset, Any]):
        max_rating (Union[Unset, Any]):
        me (Union[Unset, bool]):
        min_bpm (Union[Unset, Any]):
        min_duration (Union[Unset, int]):
        min_nps (Union[Unset, Any]):
        min_rating (Union[Unset, Any]):
        noodle (Union[Unset, bool]):
        q (Union[Unset, str]):
        sort_order (GetSearchTextPageSortOrder):
        tags (Union[Unset, str]):
        to (Union[Unset, datetime.datetime]):
        verified (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SearchResponse
    """

    return (
        await asyncio_detailed(
            page=page,
            client=client,
            automapper=automapper,
            chroma=chroma,
            cinema=cinema,
            curated=curated,
            followed=followed,
            from_=from_,
            full_spread=full_spread,
            leaderboard=leaderboard,
            max_bpm=max_bpm,
            max_duration=max_duration,
            max_nps=max_nps,
            max_rating=max_rating,
            me=me,
            min_bpm=min_bpm,
            min_duration=min_duration,
            min_nps=min_nps,
            min_rating=min_rating,
            noodle=noodle,
            q=q,
            sort_order=sort_order,
            tags=tags,
            to=to,
            verified=verified,
        )
    ).parsed
