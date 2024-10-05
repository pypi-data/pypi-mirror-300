from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.score_collection import ScoreCollection
from ...types import UNSET, Response, Unset


def _get_kwargs(
    leaderboard_id: float,
    *,
    countries: Union[Unset, str] = UNSET,
    search: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    with_metadata: Union[Unset, bool] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["countries"] = countries

    params["search"] = search

    params["page"] = page

    params["withMetadata"] = with_metadata

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/leaderboard/by-id/{leaderboard_id}/scores",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ScoreCollection]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ScoreCollection.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = cast(Any, None)
        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, ScoreCollection]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    leaderboard_id: float,
    *,
    client: Union[AuthenticatedClient, Client],
    countries: Union[Unset, str] = UNSET,
    search: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    with_metadata: Union[Unset, bool] = UNSET,
) -> Response[Union[Any, ScoreCollection]]:
    """Gets leaderboard scores by ScoreSaber leaderboardId

    Args:
        leaderboard_id (float):
        countries (Union[Unset, str]):
        search (Union[Unset, str]):
        page (Union[Unset, int]):
        with_metadata (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ScoreCollection]]
    """

    kwargs = _get_kwargs(
        leaderboard_id=leaderboard_id,
        countries=countries,
        search=search,
        page=page,
        with_metadata=with_metadata,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    leaderboard_id: float,
    *,
    client: Union[AuthenticatedClient, Client],
    countries: Union[Unset, str] = UNSET,
    search: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    with_metadata: Union[Unset, bool] = UNSET,
) -> Optional[Union[Any, ScoreCollection]]:
    """Gets leaderboard scores by ScoreSaber leaderboardId

    Args:
        leaderboard_id (float):
        countries (Union[Unset, str]):
        search (Union[Unset, str]):
        page (Union[Unset, int]):
        with_metadata (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ScoreCollection]
    """

    return sync_detailed(
        leaderboard_id=leaderboard_id,
        client=client,
        countries=countries,
        search=search,
        page=page,
        with_metadata=with_metadata,
    ).parsed


async def asyncio_detailed(
    leaderboard_id: float,
    *,
    client: Union[AuthenticatedClient, Client],
    countries: Union[Unset, str] = UNSET,
    search: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    with_metadata: Union[Unset, bool] = UNSET,
) -> Response[Union[Any, ScoreCollection]]:
    """Gets leaderboard scores by ScoreSaber leaderboardId

    Args:
        leaderboard_id (float):
        countries (Union[Unset, str]):
        search (Union[Unset, str]):
        page (Union[Unset, int]):
        with_metadata (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ScoreCollection]]
    """

    kwargs = _get_kwargs(
        leaderboard_id=leaderboard_id,
        countries=countries,
        search=search,
        page=page,
        with_metadata=with_metadata,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    leaderboard_id: float,
    *,
    client: Union[AuthenticatedClient, Client],
    countries: Union[Unset, str] = UNSET,
    search: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    with_metadata: Union[Unset, bool] = UNSET,
) -> Optional[Union[Any, ScoreCollection]]:
    """Gets leaderboard scores by ScoreSaber leaderboardId

    Args:
        leaderboard_id (float):
        countries (Union[Unset, str]):
        search (Union[Unset, str]):
        page (Union[Unset, int]):
        with_metadata (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ScoreCollection]
    """

    return (
        await asyncio_detailed(
            leaderboard_id=leaderboard_id,
            client=client,
            countries=countries,
            search=search,
            page=page,
            with_metadata=with_metadata,
        )
    ).parsed
