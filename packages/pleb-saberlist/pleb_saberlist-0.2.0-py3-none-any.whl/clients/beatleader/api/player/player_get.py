from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.leaderboard_contexts import LeaderboardContexts
from ...models.player_response_full import PlayerResponseFull
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    stats: Union[Unset, bool] = True,
    keep_original_id: Union[Unset, bool] = False,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["stats"] = stats

    params["keepOriginalId"] = keep_original_id

    json_leaderboard_context: Union[Unset, str] = UNSET
    if not isinstance(leaderboard_context, Unset):
        json_leaderboard_context = leaderboard_context.value

    params["leaderboardContext"] = json_leaderboard_context

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/player/{id}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, PlayerResponseFull]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PlayerResponseFull.from_dict(response.text)

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
) -> Response[Union[Any, PlayerResponseFull]]:
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
    stats: Union[Unset, bool] = True,
    keep_original_id: Union[Unset, bool] = False,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
) -> Response[Union[Any, PlayerResponseFull]]:
    """Get player profile

     Retrieves a Beat Saber profile data for a specific player ID.

    Args:
        id (str):
        stats (Union[Unset, bool]):  Default: True.
        keep_original_id (Union[Unset, bool]):  Default: False.
        leaderboard_context (Union[Unset, LeaderboardContexts]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PlayerResponseFull]]
    """

    kwargs = _get_kwargs(
        id=id,
        stats=stats,
        keep_original_id=keep_original_id,
        leaderboard_context=leaderboard_context,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    stats: Union[Unset, bool] = True,
    keep_original_id: Union[Unset, bool] = False,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
) -> Optional[Union[Any, PlayerResponseFull]]:
    """Get player profile

     Retrieves a Beat Saber profile data for a specific player ID.

    Args:
        id (str):
        stats (Union[Unset, bool]):  Default: True.
        keep_original_id (Union[Unset, bool]):  Default: False.
        leaderboard_context (Union[Unset, LeaderboardContexts]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PlayerResponseFull]
    """

    return sync_detailed(
        id=id,
        client=client,
        stats=stats,
        keep_original_id=keep_original_id,
        leaderboard_context=leaderboard_context,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    stats: Union[Unset, bool] = True,
    keep_original_id: Union[Unset, bool] = False,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
) -> Response[Union[Any, PlayerResponseFull]]:
    """Get player profile

     Retrieves a Beat Saber profile data for a specific player ID.

    Args:
        id (str):
        stats (Union[Unset, bool]):  Default: True.
        keep_original_id (Union[Unset, bool]):  Default: False.
        leaderboard_context (Union[Unset, LeaderboardContexts]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PlayerResponseFull]]
    """

    kwargs = _get_kwargs(
        id=id,
        stats=stats,
        keep_original_id=keep_original_id,
        leaderboard_context=leaderboard_context,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    stats: Union[Unset, bool] = True,
    keep_original_id: Union[Unset, bool] = False,
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
) -> Optional[Union[Any, PlayerResponseFull]]:
    """Get player profile

     Retrieves a Beat Saber profile data for a specific player ID.

    Args:
        id (str):
        stats (Union[Unset, bool]):  Default: True.
        keep_original_id (Union[Unset, bool]):  Default: False.
        leaderboard_context (Union[Unset, LeaderboardContexts]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PlayerResponseFull]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            stats=stats,
            keep_original_id=keep_original_id,
            leaderboard_context=leaderboard_context,
        )
    ).parsed
