from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.difficulty_status import DifficultyStatus
from ...models.leaderboard_contexts import LeaderboardContexts
from ...models.order import Order
from ...models.requirements import Requirements
from ...models.score_filter_status import ScoreFilterStatus
from ...models.score_response_with_my_score_response_with_metadata import ScoreResponseWithMyScoreResponseWithMetadata
from ...models.scores_sort_by import ScoresSortBy
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    sort_by: Union[Unset, ScoresSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 8,
    search: Union[Unset, str] = UNSET,
    diff: Union[Unset, str] = UNSET,
    mode: Union[Unset, str] = UNSET,
    requirements: Union[Unset, Requirements] = UNSET,
    score_status: Union[Unset, ScoreFilterStatus] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    type: Union[Unset, DifficultyStatus] = UNSET,
    modifiers: Union[Unset, str] = UNSET,
    stars_from: Union[Unset, float] = UNSET,
    stars_to: Union[Unset, float] = UNSET,
    time_from: Union[Unset, int] = UNSET,
    time_to: Union[Unset, int] = UNSET,
    event_id: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_sort_by: Union[Unset, str] = UNSET
    if not isinstance(sort_by, Unset):
        json_sort_by = sort_by.value

    params["sortBy"] = json_sort_by

    json_order: Union[Unset, str] = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params["page"] = page

    params["count"] = count

    params["search"] = search

    params["diff"] = diff

    params["mode"] = mode

    json_requirements: Union[Unset, str] = UNSET
    if not isinstance(requirements, Unset):
        json_requirements = requirements.value

    params["requirements"] = json_requirements

    json_score_status: Union[Unset, str] = UNSET
    if not isinstance(score_status, Unset):
        json_score_status = score_status.value

    params["scoreStatus"] = json_score_status

    json_leaderboard_context: Union[Unset, str] = UNSET
    if not isinstance(leaderboard_context, Unset):
        json_leaderboard_context = leaderboard_context.value

    params["leaderboardContext"] = json_leaderboard_context

    json_type: Union[Unset, str] = UNSET
    if not isinstance(type, Unset):
        json_type = type.value

    params["type"] = json_type

    params["modifiers"] = modifiers

    params["stars_from"] = stars_from

    params["stars_to"] = stars_to

    params["time_from"] = time_from

    params["time_to"] = time_to

    params["eventId"] = event_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/player/{id}/scores",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ScoreResponseWithMyScoreResponseWithMetadata]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ScoreResponseWithMyScoreResponseWithMetadata.from_dict(response.json())

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
) -> Response[Union[Any, ScoreResponseWithMyScoreResponseWithMetadata]]:
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
    sort_by: Union[Unset, ScoresSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 8,
    search: Union[Unset, str] = UNSET,
    diff: Union[Unset, str] = UNSET,
    mode: Union[Unset, str] = UNSET,
    requirements: Union[Unset, Requirements] = UNSET,
    score_status: Union[Unset, ScoreFilterStatus] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    type: Union[Unset, DifficultyStatus] = UNSET,
    modifiers: Union[Unset, str] = UNSET,
    stars_from: Union[Unset, float] = UNSET,
    stars_to: Union[Unset, float] = UNSET,
    time_from: Union[Unset, int] = UNSET,
    time_to: Union[Unset, int] = UNSET,
    event_id: Union[Unset, int] = UNSET,
) -> Response[Union[Any, ScoreResponseWithMyScoreResponseWithMetadata]]:
    """Retrieve player's scores

     Fetches a paginated list of scores for a specified player ID. Allows filtering by various criteria
    like date, difficulty, mode, and more.

    Args:
        id (str):
        sort_by (Union[Unset, ScoresSortBy]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 8.
        search (Union[Unset, str]):
        diff (Union[Unset, str]):
        mode (Union[Unset, str]):
        requirements (Union[Unset, Requirements]):
        score_status (Union[Unset, ScoreFilterStatus]):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        type (Union[Unset, DifficultyStatus]): Represents the difficulty status of a map.
        modifiers (Union[Unset, str]):
        stars_from (Union[Unset, float]):
        stars_to (Union[Unset, float]):
        time_from (Union[Unset, int]):
        time_to (Union[Unset, int]):
        event_id (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ScoreResponseWithMyScoreResponseWithMetadata]]
    """

    kwargs = _get_kwargs(
        id=id,
        sort_by=sort_by,
        order=order,
        page=page,
        count=count,
        search=search,
        diff=diff,
        mode=mode,
        requirements=requirements,
        score_status=score_status,
        leaderboard_context=leaderboard_context,
        type=type,
        modifiers=modifiers,
        stars_from=stars_from,
        stars_to=stars_to,
        time_from=time_from,
        time_to=time_to,
        event_id=event_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, ScoresSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 8,
    search: Union[Unset, str] = UNSET,
    diff: Union[Unset, str] = UNSET,
    mode: Union[Unset, str] = UNSET,
    requirements: Union[Unset, Requirements] = UNSET,
    score_status: Union[Unset, ScoreFilterStatus] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    type: Union[Unset, DifficultyStatus] = UNSET,
    modifiers: Union[Unset, str] = UNSET,
    stars_from: Union[Unset, float] = UNSET,
    stars_to: Union[Unset, float] = UNSET,
    time_from: Union[Unset, int] = UNSET,
    time_to: Union[Unset, int] = UNSET,
    event_id: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, ScoreResponseWithMyScoreResponseWithMetadata]]:
    """Retrieve player's scores

     Fetches a paginated list of scores for a specified player ID. Allows filtering by various criteria
    like date, difficulty, mode, and more.

    Args:
        id (str):
        sort_by (Union[Unset, ScoresSortBy]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 8.
        search (Union[Unset, str]):
        diff (Union[Unset, str]):
        mode (Union[Unset, str]):
        requirements (Union[Unset, Requirements]):
        score_status (Union[Unset, ScoreFilterStatus]):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        type (Union[Unset, DifficultyStatus]): Represents the difficulty status of a map.
        modifiers (Union[Unset, str]):
        stars_from (Union[Unset, float]):
        stars_to (Union[Unset, float]):
        time_from (Union[Unset, int]):
        time_to (Union[Unset, int]):
        event_id (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ScoreResponseWithMyScoreResponseWithMetadata]
    """

    return sync_detailed(
        id=id,
        client=client,
        sort_by=sort_by,
        order=order,
        page=page,
        count=count,
        search=search,
        diff=diff,
        mode=mode,
        requirements=requirements,
        score_status=score_status,
        leaderboard_context=leaderboard_context,
        type=type,
        modifiers=modifiers,
        stars_from=stars_from,
        stars_to=stars_to,
        time_from=time_from,
        time_to=time_to,
        event_id=event_id,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, ScoresSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 8,
    search: Union[Unset, str] = UNSET,
    diff: Union[Unset, str] = UNSET,
    mode: Union[Unset, str] = UNSET,
    requirements: Union[Unset, Requirements] = UNSET,
    score_status: Union[Unset, ScoreFilterStatus] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    type: Union[Unset, DifficultyStatus] = UNSET,
    modifiers: Union[Unset, str] = UNSET,
    stars_from: Union[Unset, float] = UNSET,
    stars_to: Union[Unset, float] = UNSET,
    time_from: Union[Unset, int] = UNSET,
    time_to: Union[Unset, int] = UNSET,
    event_id: Union[Unset, int] = UNSET,
) -> Response[Union[Any, ScoreResponseWithMyScoreResponseWithMetadata]]:
    """Retrieve player's scores

     Fetches a paginated list of scores for a specified player ID. Allows filtering by various criteria
    like date, difficulty, mode, and more.

    Args:
        id (str):
        sort_by (Union[Unset, ScoresSortBy]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 8.
        search (Union[Unset, str]):
        diff (Union[Unset, str]):
        mode (Union[Unset, str]):
        requirements (Union[Unset, Requirements]):
        score_status (Union[Unset, ScoreFilterStatus]):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        type (Union[Unset, DifficultyStatus]): Represents the difficulty status of a map.
        modifiers (Union[Unset, str]):
        stars_from (Union[Unset, float]):
        stars_to (Union[Unset, float]):
        time_from (Union[Unset, int]):
        time_to (Union[Unset, int]):
        event_id (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ScoreResponseWithMyScoreResponseWithMetadata]]
    """

    kwargs = _get_kwargs(
        id=id,
        sort_by=sort_by,
        order=order,
        page=page,
        count=count,
        search=search,
        diff=diff,
        mode=mode,
        requirements=requirements,
        score_status=score_status,
        leaderboard_context=leaderboard_context,
        type=type,
        modifiers=modifiers,
        stars_from=stars_from,
        stars_to=stars_to,
        time_from=time_from,
        time_to=time_to,
        event_id=event_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, ScoresSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 8,
    search: Union[Unset, str] = UNSET,
    diff: Union[Unset, str] = UNSET,
    mode: Union[Unset, str] = UNSET,
    requirements: Union[Unset, Requirements] = UNSET,
    score_status: Union[Unset, ScoreFilterStatus] = UNSET,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    type: Union[Unset, DifficultyStatus] = UNSET,
    modifiers: Union[Unset, str] = UNSET,
    stars_from: Union[Unset, float] = UNSET,
    stars_to: Union[Unset, float] = UNSET,
    time_from: Union[Unset, int] = UNSET,
    time_to: Union[Unset, int] = UNSET,
    event_id: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, ScoreResponseWithMyScoreResponseWithMetadata]]:
    """Retrieve player's scores

     Fetches a paginated list of scores for a specified player ID. Allows filtering by various criteria
    like date, difficulty, mode, and more.

    Args:
        id (str):
        sort_by (Union[Unset, ScoresSortBy]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 8.
        search (Union[Unset, str]):
        diff (Union[Unset, str]):
        mode (Union[Unset, str]):
        requirements (Union[Unset, Requirements]):
        score_status (Union[Unset, ScoreFilterStatus]):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        type (Union[Unset, DifficultyStatus]): Represents the difficulty status of a map.
        modifiers (Union[Unset, str]):
        stars_from (Union[Unset, float]):
        stars_to (Union[Unset, float]):
        time_from (Union[Unset, int]):
        time_to (Union[Unset, int]):
        event_id (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ScoreResponseWithMyScoreResponseWithMetadata]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            sort_by=sort_by,
            order=order,
            page=page,
            count=count,
            search=search,
            diff=diff,
            mode=mode,
            requirements=requirements,
            score_status=score_status,
            leaderboard_context=leaderboard_context,
            type=type,
            modifiers=modifiers,
            stars_from=stars_from,
            stars_to=stars_to,
            time_from=time_from,
            time_to=time_to,
            event_id=event_id,
        )
    ).parsed
