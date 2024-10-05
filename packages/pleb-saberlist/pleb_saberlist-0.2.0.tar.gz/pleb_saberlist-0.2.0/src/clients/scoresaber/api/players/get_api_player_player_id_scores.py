from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_api_player_player_id_scores_sort import GetApiPlayerPlayerIdScoresSort
from ...models.player_score_collection import PlayerScoreCollection
from ...types import UNSET, Response, Unset


def _get_kwargs(
    player_id: str,
    *,
    limit: Union[Unset, int] = UNSET,
    sort: Union[Unset, GetApiPlayerPlayerIdScoresSort] = UNSET,
    page: Union[Unset, int] = UNSET,
    with_metadata: Union[Unset, bool] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["limit"] = limit

    json_sort: Union[Unset, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params["page"] = page

    params["withMetadata"] = with_metadata

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/player/{player_id}/scores",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, PlayerScoreCollection]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PlayerScoreCollection.from_dict(response.json())

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
) -> Response[Union[Any, PlayerScoreCollection]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    player_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = UNSET,
    sort: Union[Unset, GetApiPlayerPlayerIdScoresSort] = UNSET,
    page: Union[Unset, int] = UNSET,
    with_metadata: Union[Unset, bool] = UNSET,
) -> Response[Union[Any, PlayerScoreCollection]]:
    """Gets scores by playerId

    Args:
        player_id (str):
        limit (Union[Unset, int]):
        sort (Union[Unset, GetApiPlayerPlayerIdScoresSort]):
        page (Union[Unset, int]):
        with_metadata (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PlayerScoreCollection]]
    """

    kwargs = _get_kwargs(
        player_id=player_id,
        limit=limit,
        sort=sort,
        page=page,
        with_metadata=with_metadata,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    player_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = UNSET,
    sort: Union[Unset, GetApiPlayerPlayerIdScoresSort] = UNSET,
    page: Union[Unset, int] = UNSET,
    with_metadata: Union[Unset, bool] = UNSET,
) -> Optional[Union[Any, PlayerScoreCollection]]:
    """Gets scores by playerId

    Args:
        player_id (str):
        limit (Union[Unset, int]):
        sort (Union[Unset, GetApiPlayerPlayerIdScoresSort]):
        page (Union[Unset, int]):
        with_metadata (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PlayerScoreCollection]
    """

    return sync_detailed(
        player_id=player_id,
        client=client,
        limit=limit,
        sort=sort,
        page=page,
        with_metadata=with_metadata,
    ).parsed


async def asyncio_detailed(
    player_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = UNSET,
    sort: Union[Unset, GetApiPlayerPlayerIdScoresSort] = UNSET,
    page: Union[Unset, int] = UNSET,
    with_metadata: Union[Unset, bool] = UNSET,
) -> Response[Union[Any, PlayerScoreCollection]]:
    """Gets scores by playerId

    Args:
        player_id (str):
        limit (Union[Unset, int]):
        sort (Union[Unset, GetApiPlayerPlayerIdScoresSort]):
        page (Union[Unset, int]):
        with_metadata (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PlayerScoreCollection]]
    """

    kwargs = _get_kwargs(
        player_id=player_id,
        limit=limit,
        sort=sort,
        page=page,
        with_metadata=with_metadata,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    player_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = UNSET,
    sort: Union[Unset, GetApiPlayerPlayerIdScoresSort] = UNSET,
    page: Union[Unset, int] = UNSET,
    with_metadata: Union[Unset, bool] = UNSET,
) -> Optional[Union[Any, PlayerScoreCollection]]:
    """Gets scores by playerId

    Args:
        player_id (str):
        limit (Union[Unset, int]):
        sort (Union[Unset, GetApiPlayerPlayerIdScoresSort]):
        page (Union[Unset, int]):
        with_metadata (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PlayerScoreCollection]
    """

    return (
        await asyncio_detailed(
            player_id=player_id,
            client=client,
            limit=limit,
            sort=sort,
            page=page,
            with_metadata=with_metadata,
        )
    ).parsed
