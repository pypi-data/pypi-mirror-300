from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.leaderboard_contexts import LeaderboardContexts
from ...models.leaderboard_response import LeaderboardResponse
from ...models.leaderboard_sort_by import LeaderboardSortBy
from ...models.order import Order
from ...models.score_filter_status import ScoreFilterStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort_by: Union[Unset, LeaderboardSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    score_status: Union[Unset, ScoreFilterStatus] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    countries: Union[Unset, str] = UNSET,
    search: Union[Unset, str] = UNSET,
    modifiers: Union[Unset, str] = UNSET,
    friends: Union[Unset, bool] = False,
    voters: Union[Unset, bool] = False,
    clan_tag: Union[Unset, str] = UNSET,
    prediction: Union[Unset, bool] = False,
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

    json_score_status: Union[Unset, str] = UNSET
    if not isinstance(score_status, Unset):
        json_score_status = score_status.value

    params["scoreStatus"] = json_score_status

    json_leaderboard_context: Union[Unset, str] = UNSET
    if not isinstance(leaderboard_context, Unset):
        json_leaderboard_context = leaderboard_context.value

    params["leaderboardContext"] = json_leaderboard_context

    params["countries"] = countries

    params["search"] = search

    params["modifiers"] = modifiers

    params["friends"] = friends

    params["voters"] = voters

    params["clanTag"] = clan_tag

    params["prediction"] = prediction

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/leaderboard/{id}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, LeaderboardResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = LeaderboardResponse.from_dict(response.text)

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
) -> Response[Union[Any, LeaderboardResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort_by: Union[Unset, LeaderboardSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    score_status: Union[Unset, ScoreFilterStatus] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    countries: Union[Unset, str] = UNSET,
    search: Union[Unset, str] = UNSET,
    modifiers: Union[Unset, str] = UNSET,
    friends: Union[Unset, bool] = False,
    voters: Union[Unset, bool] = False,
    clan_tag: Union[Unset, str] = UNSET,
    prediction: Union[Unset, bool] = False,
) -> Response[Union[Any, LeaderboardResponse]]:
    """Retrieve leaderboard details

     Fetches details of a leaderboard identified by its ID, with optional sorting and filtering for
    scores.

    Args:
        id (str):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        sort_by (Union[Unset, LeaderboardSortBy]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        score_status (Union[Unset, ScoreFilterStatus]):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        countries (Union[Unset, str]):
        search (Union[Unset, str]):
        modifiers (Union[Unset, str]):
        friends (Union[Unset, bool]):  Default: False.
        voters (Union[Unset, bool]):  Default: False.
        clan_tag (Union[Unset, str]):
        prediction (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, LeaderboardResponse]]
    """

    kwargs = _get_kwargs(
        id=id,
        page=page,
        count=count,
        sort_by=sort_by,
        order=order,
        score_status=score_status,
        leaderboard_context=leaderboard_context,
        countries=countries,
        search=search,
        modifiers=modifiers,
        friends=friends,
        voters=voters,
        clan_tag=clan_tag,
        prediction=prediction,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort_by: Union[Unset, LeaderboardSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    score_status: Union[Unset, ScoreFilterStatus] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    countries: Union[Unset, str] = UNSET,
    search: Union[Unset, str] = UNSET,
    modifiers: Union[Unset, str] = UNSET,
    friends: Union[Unset, bool] = False,
    voters: Union[Unset, bool] = False,
    clan_tag: Union[Unset, str] = UNSET,
    prediction: Union[Unset, bool] = False,
) -> Optional[Union[Any, LeaderboardResponse]]:
    """Retrieve leaderboard details

     Fetches details of a leaderboard identified by its ID, with optional sorting and filtering for
    scores.

    Args:
        id (str):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        sort_by (Union[Unset, LeaderboardSortBy]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        score_status (Union[Unset, ScoreFilterStatus]):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        countries (Union[Unset, str]):
        search (Union[Unset, str]):
        modifiers (Union[Unset, str]):
        friends (Union[Unset, bool]):  Default: False.
        voters (Union[Unset, bool]):  Default: False.
        clan_tag (Union[Unset, str]):
        prediction (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, LeaderboardResponse]
    """

    return sync_detailed(
        id=id,
        client=client,
        page=page,
        count=count,
        sort_by=sort_by,
        order=order,
        score_status=score_status,
        leaderboard_context=leaderboard_context,
        countries=countries,
        search=search,
        modifiers=modifiers,
        friends=friends,
        voters=voters,
        clan_tag=clan_tag,
        prediction=prediction,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort_by: Union[Unset, LeaderboardSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    score_status: Union[Unset, ScoreFilterStatus] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    countries: Union[Unset, str] = UNSET,
    search: Union[Unset, str] = UNSET,
    modifiers: Union[Unset, str] = UNSET,
    friends: Union[Unset, bool] = False,
    voters: Union[Unset, bool] = False,
    clan_tag: Union[Unset, str] = UNSET,
    prediction: Union[Unset, bool] = False,
) -> Response[Union[Any, LeaderboardResponse]]:
    """Retrieve leaderboard details

     Fetches details of a leaderboard identified by its ID, with optional sorting and filtering for
    scores.

    Args:
        id (str):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        sort_by (Union[Unset, LeaderboardSortBy]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        score_status (Union[Unset, ScoreFilterStatus]):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        countries (Union[Unset, str]):
        search (Union[Unset, str]):
        modifiers (Union[Unset, str]):
        friends (Union[Unset, bool]):  Default: False.
        voters (Union[Unset, bool]):  Default: False.
        clan_tag (Union[Unset, str]):
        prediction (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, LeaderboardResponse]]
    """

    kwargs = _get_kwargs(
        id=id,
        page=page,
        count=count,
        sort_by=sort_by,
        order=order,
        score_status=score_status,
        leaderboard_context=leaderboard_context,
        countries=countries,
        search=search,
        modifiers=modifiers,
        friends=friends,
        voters=voters,
        clan_tag=clan_tag,
        prediction=prediction,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort_by: Union[Unset, LeaderboardSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    score_status: Union[Unset, ScoreFilterStatus] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    countries: Union[Unset, str] = UNSET,
    search: Union[Unset, str] = UNSET,
    modifiers: Union[Unset, str] = UNSET,
    friends: Union[Unset, bool] = False,
    voters: Union[Unset, bool] = False,
    clan_tag: Union[Unset, str] = UNSET,
    prediction: Union[Unset, bool] = False,
) -> Optional[Union[Any, LeaderboardResponse]]:
    """Retrieve leaderboard details

     Fetches details of a leaderboard identified by its ID, with optional sorting and filtering for
    scores.

    Args:
        id (str):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        sort_by (Union[Unset, LeaderboardSortBy]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        score_status (Union[Unset, ScoreFilterStatus]):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        countries (Union[Unset, str]):
        search (Union[Unset, str]):
        modifiers (Union[Unset, str]):
        friends (Union[Unset, bool]):  Default: False.
        voters (Union[Unset, bool]):  Default: False.
        clan_tag (Union[Unset, str]):
        prediction (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, LeaderboardResponse]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            page=page,
            count=count,
            sort_by=sort_by,
            order=order,
            score_status=score_status,
            leaderboard_context=leaderboard_context,
            countries=countries,
            search=search,
            modifiers=modifiers,
            friends=friends,
            voters=voters,
            clan_tag=clan_tag,
            prediction=prediction,
        )
    ).parsed
