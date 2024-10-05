from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.leaderboard_clan_ranking_response import LeaderboardClanRankingResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["page"] = page

    params["count"] = count

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/leaderboard/clanRankings/{id}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, LeaderboardClanRankingResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = LeaderboardClanRankingResponse.from_dict(response.text)

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
) -> Response[Union[Any, LeaderboardClanRankingResponse]]:
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
) -> Response[Union[Any, LeaderboardClanRankingResponse]]:
    """Retrieve clan rankings for a leaderboard

     Fetches clan rankings for a leaderboard identified by its ID.

    Args:
        id (str):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, LeaderboardClanRankingResponse]]
    """

    kwargs = _get_kwargs(
        id=id,
        page=page,
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
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
) -> Optional[Union[Any, LeaderboardClanRankingResponse]]:
    """Retrieve clan rankings for a leaderboard

     Fetches clan rankings for a leaderboard identified by its ID.

    Args:
        id (str):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, LeaderboardClanRankingResponse]
    """

    return sync_detailed(
        id=id,
        client=client,
        page=page,
        count=count,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
) -> Response[Union[Any, LeaderboardClanRankingResponse]]:
    """Retrieve clan rankings for a leaderboard

     Fetches clan rankings for a leaderboard identified by its ID.

    Args:
        id (str):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, LeaderboardClanRankingResponse]]
    """

    kwargs = _get_kwargs(
        id=id,
        page=page,
        count=count,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
) -> Optional[Union[Any, LeaderboardClanRankingResponse]]:
    """Retrieve clan rankings for a leaderboard

     Fetches clan rankings for a leaderboard identified by its ID.

    Args:
        id (str):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, LeaderboardClanRankingResponse]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            page=page,
            count=count,
        )
    ).parsed
