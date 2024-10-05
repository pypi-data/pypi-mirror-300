from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.history_compact_response import HistoryCompactResponse
from ...models.leaderboard_contexts import LeaderboardContexts
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    count: Union[Unset, int] = 50,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_leaderboard_context: Union[Unset, str] = UNSET
    if not isinstance(leaderboard_context, Unset):
        json_leaderboard_context = leaderboard_context.value

    params["leaderboardContext"] = json_leaderboard_context

    params["count"] = count

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/player/{id}/history/compact",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, List["HistoryCompactResponse"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.text
        for response_200_item_data in _response_200:
            response_200_item = HistoryCompactResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[Any, List["HistoryCompactResponse"]]]:
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
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    count: Union[Unset, int] = 50,
) -> Response[Union[Any, List["HistoryCompactResponse"]]]:
    """Retrieve player's statistic history in a compact form

     Fetches a list of player's performance metrics subset. Use the main history endpoint for a full.

    Args:
        id (str):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        count (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['HistoryCompactResponse']]]
    """

    kwargs = _get_kwargs(
        id=id,
        leaderboard_context=leaderboard_context,
        count=count,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    count: Union[Unset, int] = 50,
) -> Optional[Union[Any, List["HistoryCompactResponse"]]]:
    """Retrieve player's statistic history in a compact form

     Fetches a list of player's performance metrics subset. Use the main history endpoint for a full.

    Args:
        id (str):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        count (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['HistoryCompactResponse']]
    """

    return sync_detailed(
        id=id,
        client=client,
        leaderboard_context=leaderboard_context,
        count=count,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    count: Union[Unset, int] = 50,
) -> Response[Union[Any, List["HistoryCompactResponse"]]]:
    """Retrieve player's statistic history in a compact form

     Fetches a list of player's performance metrics subset. Use the main history endpoint for a full.

    Args:
        id (str):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        count (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['HistoryCompactResponse']]]
    """

    kwargs = _get_kwargs(
        id=id,
        leaderboard_context=leaderboard_context,
        count=count,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    count: Union[Unset, int] = 50,
) -> Optional[Union[Any, List["HistoryCompactResponse"]]]:
    """Retrieve player's statistic history in a compact form

     Fetches a list of player's performance metrics subset. Use the main history endpoint for a full.

    Args:
        id (str):
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        count (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['HistoryCompactResponse']]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            leaderboard_context=leaderboard_context,
            count=count,
        )
    ).parsed
