from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.leaderboard_contexts import LeaderboardContexts
from ...models.maps_type import MapsType
from ...models.order import Order
from ...models.player_response_with_stats_response_with_metadata import PlayerResponseWithStatsResponseWithMetadata
from ...models.player_sort_by import PlayerSortBy
from ...models.pp_type import PpType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    sort_by: Union[Unset, PlayerSortBy] = UNSET,
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 50,
    search: Union[Unset, str] = "",
    order: Union[Unset, Order] = UNSET,
    countries: Union[Unset, str] = "",
    maps_type: Union[Unset, MapsType] = UNSET,
    pp_type: Union[Unset, PpType] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    friends: Union[Unset, bool] = False,
    pp_range: Union[Unset, str] = UNSET,
    score_range: Union[Unset, str] = UNSET,
    platform: Union[Unset, str] = UNSET,
    role: Union[Unset, str] = UNSET,
    hmd: Union[Unset, str] = UNSET,
    activity_period: Union[Unset, int] = UNSET,
    banned: Union[Unset, bool] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_sort_by: Union[Unset, str] = UNSET
    if not isinstance(sort_by, Unset):
        json_sort_by = sort_by.value

    params["sortBy"] = json_sort_by

    params["page"] = page

    params["count"] = count

    params["search"] = search

    json_order: Union[Unset, str] = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params["countries"] = countries

    json_maps_type: Union[Unset, str] = UNSET
    if not isinstance(maps_type, Unset):
        json_maps_type = maps_type.value

    params["mapsType"] = json_maps_type

    json_pp_type: Union[Unset, str] = UNSET
    if not isinstance(pp_type, Unset):
        json_pp_type = pp_type.value

    params["ppType"] = json_pp_type

    json_leaderboard_context: Union[Unset, str] = UNSET
    if not isinstance(leaderboard_context, Unset):
        json_leaderboard_context = leaderboard_context.value

    params["leaderboardContext"] = json_leaderboard_context

    params["friends"] = friends

    params["pp_range"] = pp_range

    params["score_range"] = score_range

    params["platform"] = platform

    params["role"] = role

    params["hmd"] = hmd

    params["activityPeriod"] = activity_period

    params["banned"] = banned

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/players",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, PlayerResponseWithStatsResponseWithMetadata]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PlayerResponseWithStatsResponseWithMetadata.from_dict(response.text)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, PlayerResponseWithStatsResponseWithMetadata]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, PlayerSortBy] = UNSET,
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 50,
    search: Union[Unset, str] = "",
    order: Union[Unset, Order] = UNSET,
    countries: Union[Unset, str] = "",
    maps_type: Union[Unset, MapsType] = UNSET,
    pp_type: Union[Unset, PpType] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    friends: Union[Unset, bool] = False,
    pp_range: Union[Unset, str] = UNSET,
    score_range: Union[Unset, str] = UNSET,
    platform: Union[Unset, str] = UNSET,
    role: Union[Unset, str] = UNSET,
    hmd: Union[Unset, str] = UNSET,
    activity_period: Union[Unset, int] = UNSET,
    banned: Union[Unset, bool] = UNSET,
) -> Response[Union[Any, PlayerResponseWithStatsResponseWithMetadata]]:
    """Retrieve a list of players (ranking)

     Fetches a paginated and optionally filtered list of players. Filters include sorting by performance
    points, search, country, maps type, platform, and more.

    Args:
        sort_by (Union[Unset, PlayerSortBy]):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 50.
        search (Union[Unset, str]):  Default: ''.
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        countries (Union[Unset, str]):  Default: ''.
        maps_type (Union[Unset, MapsType]):
        pp_type (Union[Unset, PpType]):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        friends (Union[Unset, bool]):  Default: False.
        pp_range (Union[Unset, str]):
        score_range (Union[Unset, str]):
        platform (Union[Unset, str]):
        role (Union[Unset, str]):
        hmd (Union[Unset, str]):
        activity_period (Union[Unset, int]):
        banned (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PlayerResponseWithStatsResponseWithMetadata]]
    """

    kwargs = _get_kwargs(
        sort_by=sort_by,
        page=page,
        count=count,
        search=search,
        order=order,
        countries=countries,
        maps_type=maps_type,
        pp_type=pp_type,
        leaderboard_context=leaderboard_context,
        friends=friends,
        pp_range=pp_range,
        score_range=score_range,
        platform=platform,
        role=role,
        hmd=hmd,
        activity_period=activity_period,
        banned=banned,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, PlayerSortBy] = UNSET,
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 50,
    search: Union[Unset, str] = "",
    order: Union[Unset, Order] = UNSET,
    countries: Union[Unset, str] = "",
    maps_type: Union[Unset, MapsType] = UNSET,
    pp_type: Union[Unset, PpType] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    friends: Union[Unset, bool] = False,
    pp_range: Union[Unset, str] = UNSET,
    score_range: Union[Unset, str] = UNSET,
    platform: Union[Unset, str] = UNSET,
    role: Union[Unset, str] = UNSET,
    hmd: Union[Unset, str] = UNSET,
    activity_period: Union[Unset, int] = UNSET,
    banned: Union[Unset, bool] = UNSET,
) -> Optional[Union[Any, PlayerResponseWithStatsResponseWithMetadata]]:
    """Retrieve a list of players (ranking)

     Fetches a paginated and optionally filtered list of players. Filters include sorting by performance
    points, search, country, maps type, platform, and more.

    Args:
        sort_by (Union[Unset, PlayerSortBy]):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 50.
        search (Union[Unset, str]):  Default: ''.
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        countries (Union[Unset, str]):  Default: ''.
        maps_type (Union[Unset, MapsType]):
        pp_type (Union[Unset, PpType]):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        friends (Union[Unset, bool]):  Default: False.
        pp_range (Union[Unset, str]):
        score_range (Union[Unset, str]):
        platform (Union[Unset, str]):
        role (Union[Unset, str]):
        hmd (Union[Unset, str]):
        activity_period (Union[Unset, int]):
        banned (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PlayerResponseWithStatsResponseWithMetadata]
    """

    return sync_detailed(
        client=client,
        sort_by=sort_by,
        page=page,
        count=count,
        search=search,
        order=order,
        countries=countries,
        maps_type=maps_type,
        pp_type=pp_type,
        leaderboard_context=leaderboard_context,
        friends=friends,
        pp_range=pp_range,
        score_range=score_range,
        platform=platform,
        role=role,
        hmd=hmd,
        activity_period=activity_period,
        banned=banned,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, PlayerSortBy] = UNSET,
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 50,
    search: Union[Unset, str] = "",
    order: Union[Unset, Order] = UNSET,
    countries: Union[Unset, str] = "",
    maps_type: Union[Unset, MapsType] = UNSET,
    pp_type: Union[Unset, PpType] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    friends: Union[Unset, bool] = False,
    pp_range: Union[Unset, str] = UNSET,
    score_range: Union[Unset, str] = UNSET,
    platform: Union[Unset, str] = UNSET,
    role: Union[Unset, str] = UNSET,
    hmd: Union[Unset, str] = UNSET,
    activity_period: Union[Unset, int] = UNSET,
    banned: Union[Unset, bool] = UNSET,
) -> Response[Union[Any, PlayerResponseWithStatsResponseWithMetadata]]:
    """Retrieve a list of players (ranking)

     Fetches a paginated and optionally filtered list of players. Filters include sorting by performance
    points, search, country, maps type, platform, and more.

    Args:
        sort_by (Union[Unset, PlayerSortBy]):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 50.
        search (Union[Unset, str]):  Default: ''.
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        countries (Union[Unset, str]):  Default: ''.
        maps_type (Union[Unset, MapsType]):
        pp_type (Union[Unset, PpType]):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        friends (Union[Unset, bool]):  Default: False.
        pp_range (Union[Unset, str]):
        score_range (Union[Unset, str]):
        platform (Union[Unset, str]):
        role (Union[Unset, str]):
        hmd (Union[Unset, str]):
        activity_period (Union[Unset, int]):
        banned (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PlayerResponseWithStatsResponseWithMetadata]]
    """

    kwargs = _get_kwargs(
        sort_by=sort_by,
        page=page,
        count=count,
        search=search,
        order=order,
        countries=countries,
        maps_type=maps_type,
        pp_type=pp_type,
        leaderboard_context=leaderboard_context,
        friends=friends,
        pp_range=pp_range,
        score_range=score_range,
        platform=platform,
        role=role,
        hmd=hmd,
        activity_period=activity_period,
        banned=banned,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, PlayerSortBy] = UNSET,
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 50,
    search: Union[Unset, str] = "",
    order: Union[Unset, Order] = UNSET,
    countries: Union[Unset, str] = "",
    maps_type: Union[Unset, MapsType] = UNSET,
    pp_type: Union[Unset, PpType] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    friends: Union[Unset, bool] = False,
    pp_range: Union[Unset, str] = UNSET,
    score_range: Union[Unset, str] = UNSET,
    platform: Union[Unset, str] = UNSET,
    role: Union[Unset, str] = UNSET,
    hmd: Union[Unset, str] = UNSET,
    activity_period: Union[Unset, int] = UNSET,
    banned: Union[Unset, bool] = UNSET,
) -> Optional[Union[Any, PlayerResponseWithStatsResponseWithMetadata]]:
    """Retrieve a list of players (ranking)

     Fetches a paginated and optionally filtered list of players. Filters include sorting by performance
    points, search, country, maps type, platform, and more.

    Args:
        sort_by (Union[Unset, PlayerSortBy]):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 50.
        search (Union[Unset, str]):  Default: ''.
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        countries (Union[Unset, str]):  Default: ''.
        maps_type (Union[Unset, MapsType]):
        pp_type (Union[Unset, PpType]):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        friends (Union[Unset, bool]):  Default: False.
        pp_range (Union[Unset, str]):
        score_range (Union[Unset, str]):
        platform (Union[Unset, str]):
        role (Union[Unset, str]):
        hmd (Union[Unset, str]):
        activity_period (Union[Unset, int]):
        banned (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PlayerResponseWithStatsResponseWithMetadata]
    """

    return (
        await asyncio_detailed(
            client=client,
            sort_by=sort_by,
            page=page,
            count=count,
            search=search,
            order=order,
            countries=countries,
            maps_type=maps_type,
            pp_type=pp_type,
            leaderboard_context=leaderboard_context,
            friends=friends,
            pp_range=pp_range,
            score_range=score_range,
            platform=platform,
            role=role,
            hmd=hmd,
            activity_period=activity_period,
            banned=banned,
        )
    ).parsed
