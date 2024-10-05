from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.leaderboard_contexts import LeaderboardContexts
from ...models.leaderboard_info_response_response_with_metadata import LeaderboardInfoResponseResponseWithMetadata
from ...models.map_sort_by import MapSortBy
from ...models.my_type import MyType
from ...models.operation import Operation
from ...models.order import Order
from ...models.requirements import Requirements
from ...models.song_status import SongStatus
from ...models.type import Type
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort_by: Union[Unset, MapSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    search: Union[Unset, str] = UNSET,
    type: Union[Unset, Type] = UNSET,
    mode: Union[Unset, str] = UNSET,
    difficulty: Union[Unset, str] = UNSET,
    map_type: Union[Unset, int] = UNSET,
    all_types: Union[Unset, Operation] = UNSET,
    map_requirements: Union[Unset, Requirements] = UNSET,
    all_requirements: Union[Unset, Operation] = UNSET,
    song_status: Union[Unset, SongStatus] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    mytype: Union[Unset, MyType] = UNSET,
    stars_from: Union[Unset, float] = UNSET,
    stars_to: Union[Unset, float] = UNSET,
    accrating_from: Union[Unset, float] = UNSET,
    accrating_to: Union[Unset, float] = UNSET,
    passrating_from: Union[Unset, float] = UNSET,
    passrating_to: Union[Unset, float] = UNSET,
    techrating_from: Union[Unset, float] = UNSET,
    techrating_to: Union[Unset, float] = UNSET,
    date_from: Union[Unset, int] = UNSET,
    date_to: Union[Unset, int] = UNSET,
    mappers: Union[Unset, str] = UNSET,
    override_current_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["page"] = page

    params["count"] = count

    json_sort_by: Union[Unset, str] = UNSET
    if not isinstance(sort_by, Unset):
        json_sort_by = sort_by.value

    params["sortBy"] = json_sort_by

    json_order: Union[Unset, str] = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params["search"] = search

    json_type: Union[Unset, str] = UNSET
    if not isinstance(type, Unset):
        json_type = type.value

    params["type"] = json_type

    params["mode"] = mode

    params["difficulty"] = difficulty

    params["mapType"] = map_type

    json_all_types: Union[Unset, str] = UNSET
    if not isinstance(all_types, Unset):
        json_all_types = all_types.value

    params["allTypes"] = json_all_types

    json_map_requirements: Union[Unset, str] = UNSET
    if not isinstance(map_requirements, Unset):
        json_map_requirements = map_requirements.value

    params["mapRequirements"] = json_map_requirements

    json_all_requirements: Union[Unset, str] = UNSET
    if not isinstance(all_requirements, Unset):
        json_all_requirements = all_requirements.value

    params["allRequirements"] = json_all_requirements

    json_song_status: Union[Unset, str] = UNSET
    if not isinstance(song_status, Unset):
        json_song_status = song_status.value

    params["songStatus"] = json_song_status

    json_leaderboard_context: Union[Unset, str] = UNSET
    if not isinstance(leaderboard_context, Unset):
        json_leaderboard_context = leaderboard_context.value

    params["leaderboardContext"] = json_leaderboard_context

    json_mytype: Union[Unset, str] = UNSET
    if not isinstance(mytype, Unset):
        json_mytype = mytype.value

    params["mytype"] = json_mytype

    params["stars_from"] = stars_from

    params["stars_to"] = stars_to

    params["accrating_from"] = accrating_from

    params["accrating_to"] = accrating_to

    params["passrating_from"] = passrating_from

    params["passrating_to"] = passrating_to

    params["techrating_from"] = techrating_from

    params["techrating_to"] = techrating_to

    params["date_from"] = date_from

    params["date_to"] = date_to

    params["mappers"] = mappers

    params["overrideCurrentId"] = override_current_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/leaderboards",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, LeaderboardInfoResponseResponseWithMetadata]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = LeaderboardInfoResponseResponseWithMetadata.from_dict(response.text)

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, LeaderboardInfoResponseResponseWithMetadata]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort_by: Union[Unset, MapSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    search: Union[Unset, str] = UNSET,
    type: Union[Unset, Type] = UNSET,
    mode: Union[Unset, str] = UNSET,
    difficulty: Union[Unset, str] = UNSET,
    map_type: Union[Unset, int] = UNSET,
    all_types: Union[Unset, Operation] = UNSET,
    map_requirements: Union[Unset, Requirements] = UNSET,
    all_requirements: Union[Unset, Operation] = UNSET,
    song_status: Union[Unset, SongStatus] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    mytype: Union[Unset, MyType] = UNSET,
    stars_from: Union[Unset, float] = UNSET,
    stars_to: Union[Unset, float] = UNSET,
    accrating_from: Union[Unset, float] = UNSET,
    accrating_to: Union[Unset, float] = UNSET,
    passrating_from: Union[Unset, float] = UNSET,
    passrating_to: Union[Unset, float] = UNSET,
    techrating_from: Union[Unset, float] = UNSET,
    techrating_to: Union[Unset, float] = UNSET,
    date_from: Union[Unset, int] = UNSET,
    date_to: Union[Unset, int] = UNSET,
    mappers: Union[Unset, str] = UNSET,
    override_current_id: Union[Unset, str] = UNSET,
) -> Response[Union[Any, LeaderboardInfoResponseResponseWithMetadata]]:
    """Retrieve a list of leaderboards (maps)

     Fetches a paginated and optionally filtered list of leaderboards (Beat Saber maps).

    Args:
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        sort_by (Union[Unset, MapSortBy]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        search (Union[Unset, str]):
        type (Union[Unset, Type]):
        mode (Union[Unset, str]):
        difficulty (Union[Unset, str]):
        map_type (Union[Unset, int]):
        all_types (Union[Unset, Operation]):
        map_requirements (Union[Unset, Requirements]):
        all_requirements (Union[Unset, Operation]):
        song_status (Union[Unset, SongStatus]):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        mytype (Union[Unset, MyType]):
        stars_from (Union[Unset, float]):
        stars_to (Union[Unset, float]):
        accrating_from (Union[Unset, float]):
        accrating_to (Union[Unset, float]):
        passrating_from (Union[Unset, float]):
        passrating_to (Union[Unset, float]):
        techrating_from (Union[Unset, float]):
        techrating_to (Union[Unset, float]):
        date_from (Union[Unset, int]):
        date_to (Union[Unset, int]):
        mappers (Union[Unset, str]):
        override_current_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, LeaderboardInfoResponseResponseWithMetadata]]
    """

    kwargs = _get_kwargs(
        page=page,
        count=count,
        sort_by=sort_by,
        order=order,
        search=search,
        type=type,
        mode=mode,
        difficulty=difficulty,
        map_type=map_type,
        all_types=all_types,
        map_requirements=map_requirements,
        all_requirements=all_requirements,
        song_status=song_status,
        leaderboard_context=leaderboard_context,
        mytype=mytype,
        stars_from=stars_from,
        stars_to=stars_to,
        accrating_from=accrating_from,
        accrating_to=accrating_to,
        passrating_from=passrating_from,
        passrating_to=passrating_to,
        techrating_from=techrating_from,
        techrating_to=techrating_to,
        date_from=date_from,
        date_to=date_to,
        mappers=mappers,
        override_current_id=override_current_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort_by: Union[Unset, MapSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    search: Union[Unset, str] = UNSET,
    type: Union[Unset, Type] = UNSET,
    mode: Union[Unset, str] = UNSET,
    difficulty: Union[Unset, str] = UNSET,
    map_type: Union[Unset, int] = UNSET,
    all_types: Union[Unset, Operation] = UNSET,
    map_requirements: Union[Unset, Requirements] = UNSET,
    all_requirements: Union[Unset, Operation] = UNSET,
    song_status: Union[Unset, SongStatus] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    mytype: Union[Unset, MyType] = UNSET,
    stars_from: Union[Unset, float] = UNSET,
    stars_to: Union[Unset, float] = UNSET,
    accrating_from: Union[Unset, float] = UNSET,
    accrating_to: Union[Unset, float] = UNSET,
    passrating_from: Union[Unset, float] = UNSET,
    passrating_to: Union[Unset, float] = UNSET,
    techrating_from: Union[Unset, float] = UNSET,
    techrating_to: Union[Unset, float] = UNSET,
    date_from: Union[Unset, int] = UNSET,
    date_to: Union[Unset, int] = UNSET,
    mappers: Union[Unset, str] = UNSET,
    override_current_id: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, LeaderboardInfoResponseResponseWithMetadata]]:
    """Retrieve a list of leaderboards (maps)

     Fetches a paginated and optionally filtered list of leaderboards (Beat Saber maps).

    Args:
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        sort_by (Union[Unset, MapSortBy]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        search (Union[Unset, str]):
        type (Union[Unset, Type]):
        mode (Union[Unset, str]):
        difficulty (Union[Unset, str]):
        map_type (Union[Unset, int]):
        all_types (Union[Unset, Operation]):
        map_requirements (Union[Unset, Requirements]):
        all_requirements (Union[Unset, Operation]):
        song_status (Union[Unset, SongStatus]):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        mytype (Union[Unset, MyType]):
        stars_from (Union[Unset, float]):
        stars_to (Union[Unset, float]):
        accrating_from (Union[Unset, float]):
        accrating_to (Union[Unset, float]):
        passrating_from (Union[Unset, float]):
        passrating_to (Union[Unset, float]):
        techrating_from (Union[Unset, float]):
        techrating_to (Union[Unset, float]):
        date_from (Union[Unset, int]):
        date_to (Union[Unset, int]):
        mappers (Union[Unset, str]):
        override_current_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, LeaderboardInfoResponseResponseWithMetadata]
    """

    return sync_detailed(
        client=client,
        page=page,
        count=count,
        sort_by=sort_by,
        order=order,
        search=search,
        type=type,
        mode=mode,
        difficulty=difficulty,
        map_type=map_type,
        all_types=all_types,
        map_requirements=map_requirements,
        all_requirements=all_requirements,
        song_status=song_status,
        leaderboard_context=leaderboard_context,
        mytype=mytype,
        stars_from=stars_from,
        stars_to=stars_to,
        accrating_from=accrating_from,
        accrating_to=accrating_to,
        passrating_from=passrating_from,
        passrating_to=passrating_to,
        techrating_from=techrating_from,
        techrating_to=techrating_to,
        date_from=date_from,
        date_to=date_to,
        mappers=mappers,
        override_current_id=override_current_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort_by: Union[Unset, MapSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    search: Union[Unset, str] = UNSET,
    type: Union[Unset, Type] = UNSET,
    mode: Union[Unset, str] = UNSET,
    difficulty: Union[Unset, str] = UNSET,
    map_type: Union[Unset, int] = UNSET,
    all_types: Union[Unset, Operation] = UNSET,
    map_requirements: Union[Unset, Requirements] = UNSET,
    all_requirements: Union[Unset, Operation] = UNSET,
    song_status: Union[Unset, SongStatus] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    mytype: Union[Unset, MyType] = UNSET,
    stars_from: Union[Unset, float] = UNSET,
    stars_to: Union[Unset, float] = UNSET,
    accrating_from: Union[Unset, float] = UNSET,
    accrating_to: Union[Unset, float] = UNSET,
    passrating_from: Union[Unset, float] = UNSET,
    passrating_to: Union[Unset, float] = UNSET,
    techrating_from: Union[Unset, float] = UNSET,
    techrating_to: Union[Unset, float] = UNSET,
    date_from: Union[Unset, int] = UNSET,
    date_to: Union[Unset, int] = UNSET,
    mappers: Union[Unset, str] = UNSET,
    override_current_id: Union[Unset, str] = UNSET,
) -> Response[Union[Any, LeaderboardInfoResponseResponseWithMetadata]]:
    """Retrieve a list of leaderboards (maps)

     Fetches a paginated and optionally filtered list of leaderboards (Beat Saber maps).

    Args:
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        sort_by (Union[Unset, MapSortBy]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        search (Union[Unset, str]):
        type (Union[Unset, Type]):
        mode (Union[Unset, str]):
        difficulty (Union[Unset, str]):
        map_type (Union[Unset, int]):
        all_types (Union[Unset, Operation]):
        map_requirements (Union[Unset, Requirements]):
        all_requirements (Union[Unset, Operation]):
        song_status (Union[Unset, SongStatus]):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        mytype (Union[Unset, MyType]):
        stars_from (Union[Unset, float]):
        stars_to (Union[Unset, float]):
        accrating_from (Union[Unset, float]):
        accrating_to (Union[Unset, float]):
        passrating_from (Union[Unset, float]):
        passrating_to (Union[Unset, float]):
        techrating_from (Union[Unset, float]):
        techrating_to (Union[Unset, float]):
        date_from (Union[Unset, int]):
        date_to (Union[Unset, int]):
        mappers (Union[Unset, str]):
        override_current_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, LeaderboardInfoResponseResponseWithMetadata]]
    """

    kwargs = _get_kwargs(
        page=page,
        count=count,
        sort_by=sort_by,
        order=order,
        search=search,
        type=type,
        mode=mode,
        difficulty=difficulty,
        map_type=map_type,
        all_types=all_types,
        map_requirements=map_requirements,
        all_requirements=all_requirements,
        song_status=song_status,
        leaderboard_context=leaderboard_context,
        mytype=mytype,
        stars_from=stars_from,
        stars_to=stars_to,
        accrating_from=accrating_from,
        accrating_to=accrating_to,
        passrating_from=passrating_from,
        passrating_to=passrating_to,
        techrating_from=techrating_from,
        techrating_to=techrating_to,
        date_from=date_from,
        date_to=date_to,
        mappers=mappers,
        override_current_id=override_current_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort_by: Union[Unset, MapSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    search: Union[Unset, str] = UNSET,
    type: Union[Unset, Type] = UNSET,
    mode: Union[Unset, str] = UNSET,
    difficulty: Union[Unset, str] = UNSET,
    map_type: Union[Unset, int] = UNSET,
    all_types: Union[Unset, Operation] = UNSET,
    map_requirements: Union[Unset, Requirements] = UNSET,
    all_requirements: Union[Unset, Operation] = UNSET,
    song_status: Union[Unset, SongStatus] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    mytype: Union[Unset, MyType] = UNSET,
    stars_from: Union[Unset, float] = UNSET,
    stars_to: Union[Unset, float] = UNSET,
    accrating_from: Union[Unset, float] = UNSET,
    accrating_to: Union[Unset, float] = UNSET,
    passrating_from: Union[Unset, float] = UNSET,
    passrating_to: Union[Unset, float] = UNSET,
    techrating_from: Union[Unset, float] = UNSET,
    techrating_to: Union[Unset, float] = UNSET,
    date_from: Union[Unset, int] = UNSET,
    date_to: Union[Unset, int] = UNSET,
    mappers: Union[Unset, str] = UNSET,
    override_current_id: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, LeaderboardInfoResponseResponseWithMetadata]]:
    """Retrieve a list of leaderboards (maps)

     Fetches a paginated and optionally filtered list of leaderboards (Beat Saber maps).

    Args:
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        sort_by (Union[Unset, MapSortBy]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        search (Union[Unset, str]):
        type (Union[Unset, Type]):
        mode (Union[Unset, str]):
        difficulty (Union[Unset, str]):
        map_type (Union[Unset, int]):
        all_types (Union[Unset, Operation]):
        map_requirements (Union[Unset, Requirements]):
        all_requirements (Union[Unset, Operation]):
        song_status (Union[Unset, SongStatus]):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        mytype (Union[Unset, MyType]):
        stars_from (Union[Unset, float]):
        stars_to (Union[Unset, float]):
        accrating_from (Union[Unset, float]):
        accrating_to (Union[Unset, float]):
        passrating_from (Union[Unset, float]):
        passrating_to (Union[Unset, float]):
        techrating_from (Union[Unset, float]):
        techrating_to (Union[Unset, float]):
        date_from (Union[Unset, int]):
        date_to (Union[Unset, int]):
        mappers (Union[Unset, str]):
        override_current_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, LeaderboardInfoResponseResponseWithMetadata]
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            count=count,
            sort_by=sort_by,
            order=order,
            search=search,
            type=type,
            mode=mode,
            difficulty=difficulty,
            map_type=map_type,
            all_types=all_types,
            map_requirements=map_requirements,
            all_requirements=all_requirements,
            song_status=song_status,
            leaderboard_context=leaderboard_context,
            mytype=mytype,
            stars_from=stars_from,
            stars_to=stars_to,
            accrating_from=accrating_from,
            accrating_to=accrating_to,
            passrating_from=passrating_from,
            passrating_to=passrating_to,
            techrating_from=techrating_from,
            techrating_to=techrating_to,
            date_from=date_from,
            date_to=date_to,
            mappers=mappers,
            override_current_id=override_current_id,
        )
    ).parsed
