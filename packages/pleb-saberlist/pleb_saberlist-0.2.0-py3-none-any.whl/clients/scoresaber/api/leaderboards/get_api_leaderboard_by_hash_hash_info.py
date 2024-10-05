from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.leaderboard_info import LeaderboardInfo
from ...types import UNSET, Response, Unset


def _get_kwargs(
    hash_: str,
    *,
    difficulty: int,
    game_mode: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["difficulty"] = difficulty

    params["gameMode"] = game_mode

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/leaderboard/by-hash/{hash_}/info",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, LeaderboardInfo]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = LeaderboardInfo.from_dict(response.json())

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
) -> Response[Union[Any, LeaderboardInfo]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    hash_: str,
    *,
    client: Union[AuthenticatedClient, Client],
    difficulty: int,
    game_mode: Union[Unset, str] = UNSET,
) -> Response[Union[Any, LeaderboardInfo]]:
    """Gets leaderboard information by map hash

    Args:
        hash_ (str):
        difficulty (int):
        game_mode (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, LeaderboardInfo]]
    """

    kwargs = _get_kwargs(
        hash_=hash_,
        difficulty=difficulty,
        game_mode=game_mode,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    hash_: str,
    *,
    client: Union[AuthenticatedClient, Client],
    difficulty: int,
    game_mode: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, LeaderboardInfo]]:
    """Gets leaderboard information by map hash

    Args:
        hash_ (str):
        difficulty (int):
        game_mode (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, LeaderboardInfo]
    """

    return sync_detailed(
        hash_=hash_,
        client=client,
        difficulty=difficulty,
        game_mode=game_mode,
    ).parsed


async def asyncio_detailed(
    hash_: str,
    *,
    client: Union[AuthenticatedClient, Client],
    difficulty: int,
    game_mode: Union[Unset, str] = UNSET,
) -> Response[Union[Any, LeaderboardInfo]]:
    """Gets leaderboard information by map hash

    Args:
        hash_ (str):
        difficulty (int):
        game_mode (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, LeaderboardInfo]]
    """

    kwargs = _get_kwargs(
        hash_=hash_,
        difficulty=difficulty,
        game_mode=game_mode,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    hash_: str,
    *,
    client: Union[AuthenticatedClient, Client],
    difficulty: int,
    game_mode: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, LeaderboardInfo]]:
    """Gets leaderboard information by map hash

    Args:
        hash_ (str):
        difficulty (int):
        game_mode (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, LeaderboardInfo]
    """

    return (
        await asyncio_detailed(
            hash_=hash_,
            client=client,
            difficulty=difficulty,
            game_mode=game_mode,
        )
    ).parsed
