from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.leaderboard_contexts import LeaderboardContexts
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    type: Union[Unset, str] = "acc",
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    no_unranked_stars: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["type"] = type

    json_leaderboard_context: Union[Unset, str] = UNSET
    if not isinstance(leaderboard_context, Unset):
        json_leaderboard_context = leaderboard_context.value

    params["leaderboardContext"] = json_leaderboard_context

    params["no_unranked_stars"] = no_unranked_stars

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/player/{id}/accgraph",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.OK:
        return None
    if response.status_code == HTTPStatus.BAD_REQUEST:
        return None
    if response.status_code == HTTPStatus.NOT_FOUND:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
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
    type: Union[Unset, str] = "acc",
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    no_unranked_stars: Union[Unset, bool] = False,
) -> Response[Any]:
    """Retrieve player's accuracy graph

     Usefull to visualise player's performance relative to map's complexity

    Args:
        id (str):
        type (Union[Unset, str]):  Default: 'acc'.
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        no_unranked_stars (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        type=type,
        leaderboard_context=leaderboard_context,
        no_unranked_stars=no_unranked_stars,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    type: Union[Unset, str] = "acc",
    leaderboard_context: Union[Unset, LeaderboardContexts] = UNSET,
    no_unranked_stars: Union[Unset, bool] = False,
) -> Response[Any]:
    """Retrieve player's accuracy graph

     Usefull to visualise player's performance relative to map's complexity

    Args:
        id (str):
        type (Union[Unset, str]):  Default: 'acc'.
        leaderboard_context (Union[Unset, LeaderboardContexts]):
        no_unranked_stars (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        type=type,
        leaderboard_context=leaderboard_context,
        no_unranked_stars=no_unranked_stars,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
