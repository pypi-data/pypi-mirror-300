from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.clan_maps_sort_by import ClanMapsSortBy
from ...models.clan_ranking_response_clan_response_full_response_with_metadata_and_container import (
    ClanRankingResponseClanResponseFullResponseWithMetadataAndContainer,
)
from ...models.leaderboard_contexts import LeaderboardContexts
from ...models.order import Order
from ...types import UNSET, Response, Unset


def _get_kwargs(
    tag: str,
    *,
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort_by: Union[Unset, ClanMapsSortBy] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    order: Union[Unset, Order] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["page"] = page

    params["count"] = count

    json_sort_by: Union[Unset, str] = UNSET
    if not isinstance(sort_by, Unset):
        json_sort_by = sort_by.value

    params["sortBy"] = json_sort_by

    json_leaderboard_context: Union[Unset, str] = UNSET
    if not isinstance(leaderboard_context, Unset):
        json_leaderboard_context = leaderboard_context.value

    params["leaderboardContext"] = json_leaderboard_context

    json_order: Union[Unset, str] = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/clan/{tag}/maps",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ClanRankingResponseClanResponseFullResponseWithMetadataAndContainer]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ClanRankingResponseClanResponseFullResponseWithMetadataAndContainer.from_dict(response.text)

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
) -> Response[Union[Any, ClanRankingResponseClanResponseFullResponseWithMetadataAndContainer]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tag: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort_by: Union[Unset, ClanMapsSortBy] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    order: Union[Unset, Order] = UNSET,
) -> Response[Union[Any, ClanRankingResponseClanResponseFullResponseWithMetadataAndContainer]]:
    """Retrieve clan maps by tag

     Fetches ranked maps(maps that can be captured on the global map) for where players of clan made
    scores identified by its tag, with optional sorting and filtering.

    Args:
        tag (str):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        sort_by (Union[Unset, ClanMapsSortBy]):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ClanRankingResponseClanResponseFullResponseWithMetadataAndContainer]]
    """

    kwargs = _get_kwargs(
        tag=tag,
        page=page,
        count=count,
        sort_by=sort_by,
        leaderboard_context=leaderboard_context,
        order=order,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    tag: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort_by: Union[Unset, ClanMapsSortBy] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    order: Union[Unset, Order] = UNSET,
) -> Optional[Union[Any, ClanRankingResponseClanResponseFullResponseWithMetadataAndContainer]]:
    """Retrieve clan maps by tag

     Fetches ranked maps(maps that can be captured on the global map) for where players of clan made
    scores identified by its tag, with optional sorting and filtering.

    Args:
        tag (str):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        sort_by (Union[Unset, ClanMapsSortBy]):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ClanRankingResponseClanResponseFullResponseWithMetadataAndContainer]
    """

    return sync_detailed(
        tag=tag,
        client=client,
        page=page,
        count=count,
        sort_by=sort_by,
        leaderboard_context=leaderboard_context,
        order=order,
    ).parsed


async def asyncio_detailed(
    tag: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort_by: Union[Unset, ClanMapsSortBy] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    order: Union[Unset, Order] = UNSET,
) -> Response[Union[Any, ClanRankingResponseClanResponseFullResponseWithMetadataAndContainer]]:
    """Retrieve clan maps by tag

     Fetches ranked maps(maps that can be captured on the global map) for where players of clan made
    scores identified by its tag, with optional sorting and filtering.

    Args:
        tag (str):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        sort_by (Union[Unset, ClanMapsSortBy]):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ClanRankingResponseClanResponseFullResponseWithMetadataAndContainer]]
    """

    kwargs = _get_kwargs(
        tag=tag,
        page=page,
        count=count,
        sort_by=sort_by,
        leaderboard_context=leaderboard_context,
        order=order,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tag: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort_by: Union[Unset, ClanMapsSortBy] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    order: Union[Unset, Order] = UNSET,
) -> Optional[Union[Any, ClanRankingResponseClanResponseFullResponseWithMetadataAndContainer]]:
    """Retrieve clan maps by tag

     Fetches ranked maps(maps that can be captured on the global map) for where players of clan made
    scores identified by its tag, with optional sorting and filtering.

    Args:
        tag (str):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        sort_by (Union[Unset, ClanMapsSortBy]):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ClanRankingResponseClanResponseFullResponseWithMetadataAndContainer]
    """

    return (
        await asyncio_detailed(
            tag=tag,
            client=client,
            page=page,
            count=count,
            sort_by=sort_by,
            leaderboard_context=leaderboard_context,
            order=order,
        )
    ).parsed
